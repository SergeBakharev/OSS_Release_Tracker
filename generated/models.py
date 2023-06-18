from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///release_tracker.db'
db = SQLAlchemy(app)


class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    last_polled = db.Column(db.DateTime)
    notes = db.Column(db.Text)

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