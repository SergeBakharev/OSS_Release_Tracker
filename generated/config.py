import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Polling configuration
    POLL_FREQUENCY = int(os.environ.get('POLL_FREQUENCY', 3600))

    # Slack configuration
    SLACK_API_KEY = os.environ.get('SLACK_API_KEY')
    SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')