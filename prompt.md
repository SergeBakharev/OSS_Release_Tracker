# OSS Release Tracker Specification

## Overview

The purpose of this system is to efficiently track software releases from vendors that publish their software on container or GitHub repositories. The is implemented in Python Flask with data stored in a SQLite3 database.

## Functional Requirements
### Objects

1. **Add/Remove/Update Repositories:** The system should allow CRUD (Create, Read, Update, Delete) operations on repository records. Each repository record will include the following fields:
    - Repo ID (auto-generated)
    - Name
    - Date Added
    - URL
    - Type (github, git, or container)
    - last_polled
    - Notes

2. **Releases:** The system should allow CRUD of releases associated to each repository. Each repository can have multiple releases. Each release will have the following fields:
    - Date
    - Version
    - Notes
    - URL
    - Hash

3. **Configuration:** The system should use environment variables for it's configuration. This should include configurable items like:
    - Poll frequency
    - Slack api key
    - Slack Channel

### Release Tracking

The core application functionality is the ability to poll and populate the releases in the database for each repository tracked. This is done by polling the repositories and retrieving the list of releases via api. Each time a successful poll is completed it should update the last_polled datetime of the repository.

For repositories of type github this means checking the github releases for the repository. This should use the PyGithub library to interact with github.

For repositories of type git this means checking the git tags repository. This should be done using the gitpython library.

For container registry repositories this means retrieving a list of images tags. Only consider container image tags that are in semver format. Container tags can be retrieved using the registry api endpoint "http://{registry}/v2/{repo}/tags/list". Here is an example using curl:

``` bash
$ curl -s 'https://registry.hub.docker.com/v2/repositories/library/debian/tags'
{"count":1755,"next":"https://registry.hub.docker.com/v2/repositories/library/debian/tags?page=2\u0026page_size=2","previous":null,"results":[{"creator":621950,"id":5956353,"images":[{"architecture":"amd64","features":"","variant":null,"digest":"sha256:9340772107855de9351e88e3ba2636d045f730e05b177c5313613894c223b4d4","os":"linux","os_features":"","os_version":null,"size":29124691,"status":"active","last_pulled":"2023-06-17T01:02:17.603158Z","last_pushed":"2023-06-12T23:58:09.075548Z"},{"architecture":"s390x","features":"","variant":null,"digest":"sha256:eee0d222c03513dcdf8f3a12c6c342add8a6161af09bcb9a38eef9ef7d486122","os":"linux","os_features":"","os_version":null,"size":27490253,"status":"active","last_pulled":"2023-06-16T07:34:00.087434Z","last_pushed":"2023-06-13T04:58:23.89489Z"}],"last_updated":"2023-06-13T04:58:31.821511Z","last_updater":1156886,"last_updater_username":"doijanky","name":"unstable-slim","repository":6315,"full_size":29124691,"v2":true,"tag_status":"active","tag_last_pulled":"2023-06-17T01:02:17.603158Z","tag_last_pushed":"2023-06-13T04:58:31.821511Z","media_type":"application/vnd.docker.distribution.manifest.list.v2+json","content_type":"image","digest":"sha256:2ae17aff4c3c8cdb2d3d9c885d7c59ad518bffc89e8351598ff1f3f918183b7c"},{"creator":1156886,"id":456210846,"images":[{"architecture":"amd64","features":"","variant":null,"digest":"sha256:9340772107855de9351e88e3ba2636d045f730e05b177c5313613894c223b4d4","os":"linux","os_features":"","os_version":null,"size":29124691,"status":"active","last_pulled":"2023-06-17T01:02:17.603158Z","last_pushed":"2023-06-12T23:58:09.075548Z"},{"architecture":"s390x","features":"","variant":null,"digest":"sha256:eee0d222c03513dcdf8f3a12c6c342add8a6161af09bcb9a38eef9ef7d486122","os":"linux","os_features":"","os_version":null,"size":27490253,"status":"active","last_pulled":"2023-06-16T07:34:00.087434Z","last_pushed":"2023-06-13T04:58:23.89489Z"}],"last_updated":"2023-06-13T04:58:26.736918Z","last_updater":1156886,"last_updater_username":"doijanky","name":"unstable-20230612-slim","repository":6315,"full_size":29124691,"v2":true,"tag_status":"active","tag_last_pulled":"2023-06-17T01:02:17.603158Z","tag_last_pushed":"2023-06-13T04:58:26.736918Z","media_type":"application/vnd.docker.distribution.manifest.list.v2+json","content_type":"image","digest":"sha256:2ae17aff4c3c8cdb2d3d9c885d7c59ad518bffc89e8351598ff1f3f918183b7c"}]}

```

### Notifications

The system should send release notifications using Slack to a configurable channel if it is a new release. A single channel should be used for all notifications.

### Deployment

The system should be designed run as a docker container.

## Testing

The code has unit tests written in pytest. Separate unit test files are used for each feature.

## User Interface

The follow are the pages that should be present in the frontend:

1. **Repository List View:** The default page. It should show a list where users can see all repositories, any notes about them, and their latest release version. This list should support sorting and filtering options. It should link to the relevant other pages.

2. **Repository Detail View:** Shows the detailed information about a specific repository showing a complete list of releases.

3. **Repository Add:** Shows a form for adding a new repository

4. **Repository Update:** Shows a form for updating a existing repository's details

## Non-Functional Requirements

1. **Performance:** The system should be able to handle a large number of repositories, with quick response times for database queries.

2. **Usability:** The interface should be user-friendly, making it easy for users to navigate through different views and perform actions.

3. **Scalability:** The system should be scalable to support the addition of new repositories and users.

## Technology Stack

- Python
- SQLite3
- Flask
- PyGithub
- gitpython
