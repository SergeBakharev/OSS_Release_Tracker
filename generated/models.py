from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    last_polled = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    releases = db.relationship('Release', backref='repository', lazy=True)

    @property
    def latest_release(self):
        return self.releases.order_by(Release.date.desc()).first()

    def __repr__(self):
        return f"Repository('{self.name}', '{self.url}')"


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    url = db.Column(db.String(200))
    hash = db.Column(db.String(100))
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'), nullable=False)

    def __repr__(self):
        return f"Release('{self.version}', '{self.date}')"