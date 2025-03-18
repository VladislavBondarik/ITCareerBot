import sqlite3
from threading import Lock


class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = Lock()
        self.create_table()

    def create_table(self):
        with self.lock:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    preferences TEXT,
                    recommended_language TEXT
                )
            ''')
            self.conn.commit()

    def save_user(self, user_id, username, preferences, language):
        with self.lock:
            self.cursor.execute(
                "INSERT OR REPLACE INTO users (user_id, username, preferences, recommended_language) VALUES (?, ?, ?, "
                "?)",
                (user_id, username, preferences, language)
            )
            self.conn.commit()

    def get_user(self, user_id):
        with self.lock:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()

    def close(self):
        self.conn.close()


db = Database()
