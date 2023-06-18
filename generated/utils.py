from datetime import datetime
from github import Github
from slack_sdk import WebClient
from database import db
from git import Repo
from models import Release
from config import Config
import requests
import re


def poll_github_releases(repository):
    g = Github()
    repo = g.get_repo(repository.url)
    releases = repo.get_releases()
    for release in releases:
        release_date = release.created_at
        release_version = release.tag_name
        release_notes = release.body
        release_url = release.html_url
        release_hash = None
        new_release = Release(date=release_date, version=release_version, notes=release_notes, url=release_url, hash=release_hash, repository=repository)
        db.session.add(new_release)
    repository.last_polled = datetime.utcnow()
    db.session.commit()

def poll_git_tags(repository):
    repo = Repo(repository.url)
    tags = repo.tags
    for tag in tags:
        release_date = tag.commit.committed_datetime
        release_version = tag.name
        release_notes = None
        release_url = None
        release_hash = tag.commit.hexsha
        new_release = Release(date=release_date, version=release_version, notes=release_notes, url=release_url, hash=release_hash, repository=repository)
        db.session.add(new_release)
    repository.last_polled = datetime.utcnow()
    db.session.commit()

def poll_container_tags(repository):
    registry = repository.url.split('/')[0]
    repo_name = '/'.join(repository.url.split('/')[1:])
    url = f'https://{registry}/v2/{repo_name}/tags/list'
    response = requests.get(url)
    if response.status_code == 200:
        tags = response.json().get('results', [])
        for tag in tags:
            if is_semver(tag):
                release_date = datetime.utcnow()
                release_version = tag
                release_notes = None
                release_url = None
                release_hash = None
                new_release = Release(date=release_date, version=release_version, notes=release_notes, url=release_url, hash=release_hash, repository=repository)
                db.session.add(new_release)
        repository.last_polled = datetime.utcnow()
        db.session.commit()

def is_semver(tag):
    pattern = r'^\d+\.\d+\.\d+([-.]\w+)*$'
    return re.match(pattern, tag) is not None


def send_slack_notification(repository, release):
    # Set up your Slack API token and channel information
    slack_token = Config.SLACK_TOKEN
    channel_id = Config.SLACK_CHANNEL_ID

    # Create a Slack client
    client = WebClient(token=slack_token)

    # Compose the notification message
    message = f"New release of {repository}: {release} is now available!"

    # Send the message to the Slack channel
    response = client.chat_postMessage(channel=channel_id, text=message)

    # Check if the message was sent successfully
    if response['ok']:
        print("Release notification sent to Slack successfully!")
    else:
        print("Failed to send release notification to Slack.")
        print(response['error'])
