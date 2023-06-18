import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_tables(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create repositories table
        c.execute('''CREATE TABLE IF NOT EXISTS repositories
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      date_added TEXT NOT NULL,
                      url TEXT NOT NULL,
                      type TEXT NOT NULL,
                      last_polled TEXT,
                      notes TEXT)''')

        # Create releases table
        c.execute('''CREATE TABLE IF NOT EXISTS releases
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      repository_id INTEGER NOT NULL,
                      date TEXT NOT NULL,
                      version TEXT NOT NULL,
                      notes TEXT,
                      url TEXT,
                      hash TEXT,
                      FOREIGN KEY (repository_id) REFERENCES repositories (id))''')

        conn.commit()
        conn.close()

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