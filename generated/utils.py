import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from github import Github
from git import Repo
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///release_tracker.db'
db = SQLAlchemy(app)

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    url = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    last_polled = db.Column(db.DateTime)
    notes = db.Column(db.Text)

class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    version = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    url = db.Column(db.String(200))
    hash = db.Column(db.String(100))
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'), nullable=False)
    repository = db.relationship('Repository', backref=db.backref('releases', lazy=True))

@app.route('/')
def repository_list():
    repositories = Repository.query.all()
    return render_template('repository_list.html', repositories=repositories)

@app.route('/repository/<int:repository_id>')
def repository_detail(repository_id):
    repository = Repository.query.get(repository_id)
    return render_template('repository_detail.html', repository=repository)

@app.route('/repository/add', methods=['GET', 'POST'])
def repository_add():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        type = request.form['type']
        notes = request.form['notes']
        repository = Repository(name=name, url=url, type=type, notes=notes)
        db.session.add(repository)
        db.session.commit()
        return redirect(url_for('repository_list'))
    return render_template('repository_add.html')

@app.route('/repository/<int:repository_id>/update', methods=['GET', 'POST'])
def repository_update(repository_id):
    repository = Repository.query.get(repository_id)
    if request.method == 'POST':
        repository.name = request.form['name']
        repository.url = request.form['url']
        repository.type = request.form['type']
        repository.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('repository_list'))
    return render_template('repository_update.html', repository=repository)

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
    # Check if tag is in semver format
    return True

def send_slack_notification(repository, release):
    # Send release notification to Slack channel
    pass

if __name__ == '__main__':
    app.run(debug=True)