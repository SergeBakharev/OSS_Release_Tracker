import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = db

    def create_tables(self):
        self.db.create_all()

    def add_repository(self, name, date_added, url, type, notes):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''INSERT INTO repositories (name, date_added, url, type, notes)
                     VALUES (?, ?, ?, ?, ?)''', (name, date_added, url, type, notes))

        conn.commit()
        conn.close()

    def get_all_repositories(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''SELECT * FROM repositories''')
        repositories = c.fetchall()

        conn.close()

        return repositories

    def get_repository_by_id(self, repository_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''SELECT * FROM repositories WHERE id = ?''', (repository_id,))
        repository = c.fetchone()

        conn.close()

        return repository

    def update_repository(self, repository_id, name, url, notes):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''UPDATE repositories SET name = ?, url = ?, notes = ? WHERE id = ?''',
                  (name, url, notes, repository_id))

        conn.commit()
        conn.close()

    def delete_repository(self, repository_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''DELETE FROM repositories WHERE id = ?''', (repository_id,))

        conn.commit()
        conn.close()

    def add_release(self, repository_id, date, version, notes, url, hash):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''INSERT INTO releases (repository_id, date, version, notes, url, hash)
                     VALUES (?, ?, ?, ?, ?, ?)''', (repository_id, date, version, notes, url, hash))

        conn.commit()
        conn.close()

    def get_releases_by_repository_id(self, repository_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''SELECT * FROM releases WHERE repository_id = ?''', (repository_id,))
        releases = c.fetchall()

        conn.close()

        return releases

    def delete_release(self, release_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''DELETE FROM releases WHERE id = ?''', (release_id,))

        conn.commit()
        conn.close()