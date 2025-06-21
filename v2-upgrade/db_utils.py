import sqlite3
import bcrypt

class db_management:
    def __init__(self):
        self.db_path = "v2-upgrade/store.db"

    def create_users(self, username, password, role):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
        
            cursor.execute("INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                        (username, hashed, role))
            conn.commit()
        
            print("User created")