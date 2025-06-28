import sqlite3
import bcrypt
from config import DB_PATH, admin_user, admin_pass

def initialize_db(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Create users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT CHECK(role IN ('admin', 'manager', 'employee')) NOT NULL,
                is_deleted BIT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Create products
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                stock INTEGER DEFAULT 0 CHECK(stock >= 0),
                is_removed BIT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Create general sales tables, only total price
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_price REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')

        # Create sale_items, detail sale.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price_per_unit REAL NOT NULL,
                FOREIGN KEY(sale_id) REFERENCES sales(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            );
        ''')

        # Create activity_log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action_type TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')

        conn.commit()
    init_admin_user()
    print("Database initialized successfully.")


def init_admin_user():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if any users exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    count = cursor.fetchone()[0]

    if count == 0:
        username = admin_user
        role = "admin"
        hashed = bcrypt.hashpw(admin_pass.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                       (username, hashed, role))
        conn.commit()
        print("✅ Default admin user created.")
    else:
        print("✅ User as admin already exist, no admin created.")

    conn.close()

if __name__ == "__main__":
    initialize_db()
    