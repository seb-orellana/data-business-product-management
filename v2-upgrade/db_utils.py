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

    def add_product(self, name, price, stock):       
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                        (name, price, stock))
            conn.commit()

            print("Product added")

    def sell_products(self, user_id, items):
        """
        items: list of dicts like [{"product_id": 1, "quantity": 2}, ...]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            total_price = 0
            sale_items_data = []

            for item in items:
                cursor.execute("SELECT stock, price FROM products WHERE id = ?", (item["product_id"],))
                result = cursor.fetchone()

                if result is None:
                    print(f"❌ Product ID {item['product_id']} not found.")
                    return

                stock, price = result
                if stock < item["quantity"]:
                    print(f"❌ Not enough stock for product ID {item['product_id']}. Available: {stock}")
                    return

                # Prepare to update stock and record sale
                new_stock = stock - item["quantity"]
                cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, item["product_id"]))

                total_price += price * item["quantity"]
                sale_items_data.append((item["product_id"], item["quantity"], price))

            cursor.execute("INSERT INTO sales (user_id, total_price) VALUES (?, ?)", (user_id, total_price))
            sale_id = cursor.lastrowid

            # Insert each sale item
            for product_id, quantity, price in sale_items_data:
                cursor.execute(
                    "INSERT INTO sale_items (sale_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)",
                    (sale_id, product_id, quantity, price)
                )   

            conn.commit()

            print(f"Sold complete. Total price: {total_price:.2f}")