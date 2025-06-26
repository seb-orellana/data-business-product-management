import sqlite3
import bcrypt
from config import DB_PATH

class db_management:
    def __init__(self):
        self.db_path = DB_PATH

    def create_users(self, user_id, username, password, role):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        action_type = "create_users"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
        
            cursor.execute("INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                        (username, hashed, role))
            
            id = cursor.lastrowid
            
            msg = f"Created user {username} with role {role}."

            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()
        
            print("User created")

    def delete_user(self, user_id, user_target_id):
        action_type = "delete_user"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
        
            cursor.execute("SELECT username FROM users WHERE id = ?", (user_target_id,))
            result = cursor.fetchone()
            archived_username = f"{result[0]}_del_{user_target_id}"

            cursor.execute("UPDATE users SET username = ?, is_deleted = ? WHERE id = ?",
                            (archived_username, 1, user_target_id))

            msg = f"Deleted user: {result[0]}."
            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()
        
            print("User deleted")

    def add_product(self, user_id, name, price, stock):      
        action_type = "add_product" 
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                        (name, price, stock))
            
            id = cursor.lastrowid

            msg = f"Added product ({id}): {name} with price: {price} and stock: {stock}."

            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()

            print("Product added")

    def remove_product(self, user_id, product_id):      
        action_type = "remove_product" 
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("UPDATE products SET is_removed = ? WHERE id = ?", (1, product_id))
            
            msg = f"Removed product ({product_id})."

            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()

            print("Product removed")

    def sell_products(self, user_id, items):
        """
        items: list of dicts like [{"product_id": 1, "quantity": 2}, ...]
        """
        action_type = "sell_products" 
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            total_price = 0
            total_quantity = 0
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

                total_quantity += item["quantity"]
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

            msg = f"Selled ({sale_id}) {total_quantity} products for ${total_price}."
            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()

            print(f"Sold complete. Total price: {total_price:.2f}")

    def update_stock(self, user_id, product_id, new_stock):
        action_type = "update_stock" 
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()

            if result is None:
                print("❌ Product not found.")
                return

            cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))

            msg = f"Updated stock for product ({product_id}): '{result[0]}' updated to {new_stock}."
            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()

            print(f"✅ Stock for product '{result[0]}' updated to {new_stock}.")

    def adjust_stock(self, user_id, product_id, delta):
        action_type = "adjust_stock" 
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name, stock FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()

            if result is None:
                print("❌ Product not found.")
                return

            name, current_stock = result
            new_stock = current_stock + delta

            if new_stock < 0:
                print(f"❌ Cannot reduce below zero. Current stock: {current_stock}")
                return

            cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))

            msg = f"Adjusted stock for product ({product_id}): '{result[0]}' updated to {new_stock}."
            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()

            print(f"✅ Stock for product '{name}' adjusted by {delta}. New stock: {new_stock}")

    def update_price(self, user_id, product_id, new_price):
        action_type = "update_price" 
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name, stock FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()

            if result is None:
                print("❌ Product not found.")
                return

            cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))

            msg = f"Updated price for product ({product_id}): '{result[0]}' updated to ${new_price}."
            cursor.execute("INSERT INTO activity_log (user_id, action_type, action) VALUES (?, ?, ?)",
                        (user_id, action_type, msg))

            conn.commit()

            print(f"✅ Updated price for product '{result[0]}' to ${new_price}.")