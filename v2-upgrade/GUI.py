import tkinter as tk
from tkinter import messagebox, ttk
from config import DB_PATH
import sqlite3
from db_utils import db_management
from activityGUI import ActivityLogViewer
from sellProduct import SellProductsWindow

class BusinessGUI:
    def __init__(self, root, id, username, role):
        self.user = {"id": id, "username": username, "role": role}

        self.root = root
        self.root.geometry("300x400")
        self.root.title("Business Management")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=15, pady=15)

        self.build_interface()

    def build_interface(self):
        tk.Label(self.main_frame, text=f"Logged in as: {self.user['username']} ({self.user['role']})").grid(row=0, column=0, columnspan=2)

        # Admin-only features
        if self.user['role'] == 'admin':
            tk.Button(self.main_frame, text="Create User", command=self.create_user_window).grid(row=1, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Delete User", command=self.delete_user_window).grid(row=2, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Activity Log", command=self.open_activity_log_viewer).grid(row=3, column=0, sticky='ew')

        if self.user['role'] == 'admin' or self.user['role'] == 'manager':
            tk.Button(self.main_frame, text="Add Product", command=self.add_product_window).grid(row=4, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Remove Product", command=self.remove_product_window).grid(row=5, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Update Stock", command=self.update_stock_window).grid(row=6, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Update Price", command=self.update_price_window).grid(row=7, column=0, sticky='ew')
            tk.Button(self.main_frame, text="View Stadistics", command=self.stadistics_window).grid(row=7, column=0, sticky='ew')

        # Common features
        tk.Button(self.main_frame, text="Sell Products", command=self.sell_products_window).grid(row=8, column=0, sticky='ew')
        tk.Button(self.main_frame, text="Adjust Stock", command=self.adjust_stock_window).grid(row=9, column=0, sticky='ew')
        tk.Button(self.main_frame, text="View Products", command=self.view_products_window).grid(row=10, column=0, sticky='ew')
        tk.Button(self.main_frame, text="Change Password", command=self.change_pwsd_window).grid(row=12, column=0, sticky='ew')

    def create_user_window(self):
        db = db_management()

        win = tk.Toplevel(self.root)
        win.title("Create User")
        fields = ["Username", "Password"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(win, text=field).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[field] = entry
        tk.Label(win, text="Role").grid(row=2, column=0)
        role = tk.StringVar()
        combo = ttk.Combobox(
            win,
            textvariable=role,
            values=["admin", "manager", "employee"],
            state="readonly",
            width=18
        )
        combo.current(2)  # Default to "employee"
        combo.grid(row=2, column=1)

        def submit():
            data = {field: entries[field].get() for field in fields}

            try:
                db.create_users(self.user["id"], data["Username"], data["Password"], role.get())
                messagebox.showinfo("Info", f"User {data['Username']} created")
                win.destroy()

            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: users.username" in str(e):
                    messagebox.showerror("Error", f"The username '{data['Username']}' is already taken.")
                else:
                    messagebox.showerror("Database Error", f"Integrity error: {e}")

            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        tk.Button(win, text="Submit", command=submit).grid(row=3, columnspan=2)

    def delete_user_window(self):
        win = tk.Toplevel(self.root)
        win.title("Delete User")

        tk.Label(win, text="Select a user to delete:").pack(pady=5)

        listbox = tk.Listbox(win, width=40, height=10)
        listbox.pack(padx=10, pady=5)

        user_id_map = {}
        def load_users():
            listbox.delete(0, tk.END)
            user_id_map.clear()

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, role FROM users WHERE id <> ? AND is_deleted = 0", (1,))
                users = cursor.fetchall()

            for i, (uid, uname, role) in enumerate(users):
                listbox.insert(tk.END, f"{uname} ({role})")
                user_id_map[i] = (uid, uname)

        def confirm_deletion():
            db = db_management()
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a user to delete.")
                return

            idx = selection[0]
            user_id, username = user_id_map[idx]
            
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this user: {username}?")
            if not confirm:
                return

            try:
                db.delete_user(self.user["id"], user_id)
                messagebox.showinfo("Deleted", f"User {username} deleted successfully.")
                load_users()  # refresh listbox in-place
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(win, text="Delete Selected User", command=confirm_deletion).pack(pady=10)
        load_users()

    def change_pwsd_window(self):
        win = tk.Toplevel(self.root)
        win.title("Change password")
        tk.Label(win, text= f"Change password for {self.user['username']}").grid(row=0, columnspan=2, pady=5)
        tk.Label(win, text= "New password:").grid(row=1, column=0, pady=5)
        tk.Label(win, text= "Verify password:").grid(row=2, column=0, pady=5)
        password1 = tk.StringVar()
        password2 = tk.StringVar()
        tk.Entry(win, textvariable=password1, show="*").grid(row=1, column=1, pady=5)
        tk.Entry(win, textvariable=password2, show="*").grid(row=2, column=1, pady=5)

        def change_pwsd():
            db = db_management()
            pwsd1 = password1.get().strip()
            pwsd2 = password2.get().strip()
            if pwsd1==pwsd2:

                if pwsd1 == '':
                    messagebox.showerror("Error", f"Passwords must NOT be empty")
                else:
                    try:
                        db.change_password(self.user["id"], self.user["username"], pwsd1 )
                        messagebox.showinfo("Info", f"Password changed successfully.")
                        win.destroy()

                    except sqlite3.IntegrityError as e:
                        messagebox.showerror("Database Error", f"Integrity error: {e}")

                    except Exception as e:
                        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            else:
                messagebox.showerror("Error", f"Both passwords must be the same")

        tk.Button(win, text='Submit', command=change_pwsd).grid(row=3, columnspan=2, pady=5)

    def add_product_window(self):
        db = db_management()
        win = tk.Toplevel(self.root)
        win.title("Add Product")
        fields = ["Name", "Price", "Stock"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(win, text=field).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[field] = entry

        def submit():
            try:
                data = {field: entries[field].get().strip() for field in fields}

                # Validation for price and stock
                try:
                    price = float(data["Price"])
                    stock = int(data["Stock"])
                    if price <= 0 or stock < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Input Error", "Price must be a positive number and Stock must be a non-negative integer.")
                    return
                db.add_product(self.user["id"], data["Name"], price, stock)
                messagebox.showinfo("Info", f"Product '{data['Name']}' added successfully.")
                win.destroy()

            except sqlite3.IntegrityError as e:
                messagebox.showerror("Database Error", f"Integrity error: {e}")

            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        tk.Button(win, text="Submit", command=submit).grid(row=len(fields), columnspan=2)

    def remove_product_window(self):
        win = tk.Toplevel(self.root)
        win.title("Remove product")

        tk.Label(win, text="Select a product to remove:").pack(pady=5)

        listbox = tk.Listbox(win, width=40, height=10)
        listbox.pack(padx=10, pady=5)

        product_id_map = {}
        def load_products():
            listbox.delete(0, tk.END)
            product_id_map.clear()

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, stock FROM products WHERE is_removed = 0")
                products = cursor.fetchall()

            for i, (pid, name, stock) in enumerate(products):
                listbox.insert(tk.END, f"{pid}: {name} ({stock})")
                product_id_map[i] = (pid, name)

        def confirm_deletion():
            db = db_management()
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a product to remove.")
                return

            idx = selection[0]
            product_id, name = product_id_map[idx]
            
            confirm = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove the product: {name}?")
            if not confirm:
                return

            try:
                db.remove_product(self.user["id"], product_id)
                messagebox.showinfo("Removed", f"Product {name} removed successfully.")
                load_products()  # refresh listbox in-place
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(win, text="Delete Selected Product", command=confirm_deletion).pack(pady=10)
        load_products()

    def sell_products_window(self):
        SellProductsWindow(self.root, self.user)

    def update_stock_window(self):
        win = tk.Toplevel(self.root)
        win.title("Update stock")

        tk.Label(win, text="Select a product to update:").pack(pady=5)

        listbox = tk.Listbox(win, width=40, height=10)
        listbox.pack(padx=10, pady=5)

        product_id_map = {}
        def load_products():
            listbox.delete(0, tk.END)
            product_id_map.clear()

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, stock FROM products WHERE is_removed = 0")
                products = cursor.fetchall()

            for i, (pid, name, stock) in enumerate(products):
                listbox.insert(tk.END, f"{pid}: {name} ({stock})")
                product_id_map[i] = (pid, name, stock)

        def confirm_update(win, entry, product_id, name):
            db = db_management()
            new_stock = entry.get().strip() 
            try:
                try:
                    stock = int(new_stock)
                    if stock < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Input Error", "Stock must be a non-negative integer.")
                    return

                db.update_stock(self.user["id"], product_id, new_stock)
                messagebox.showinfo("Updated", f"Product {name} updated successfully.")
                win.destroy()
                load_products()  # refresh listbox in-place
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        def initiate_update():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a product to update.")
                return

            idx = selection[0]
            product_id, name, stock = product_id_map[idx]

            win2 = tk.Toplevel(win)
            win2.title("Update Stock Info")

            tk.Label(win2, text=f"Product: {name}").grid(row=0, column=0, columnspan=2, pady=5)
            tk.Label(win2, text=f"Current stock: {stock}").grid(row=1, column=0, columnspan=2, pady=5)
            tk.Label(win2, text="New stock:").grid(row=2, column=0, pady=5)
            entry = tk.Entry(win2)
            entry.grid(row=2, column=1, pady=5)

            tk.Button(win2, text="Update", command=lambda:confirm_update(win2, entry, product_id, name)).grid(row=3, columnspan=2, pady=5)

        tk.Button(win, text="Update Selected Product", command=initiate_update).pack(pady=10)
        load_products()

    def adjust_stock_window(self):
        win = tk.Toplevel(self.root)
        win.title("Adjust Stock")

        tk.Label(win, text="Select a product to adjust:").pack(pady=5)

        listbox = tk.Listbox(win, width=40, height=10)
        listbox.pack(padx=10, pady=5)

        product_id_map = {}

        def load_products():
            listbox.delete(0, tk.END)
            product_id_map.clear()

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, stock FROM products WHERE is_removed = 0")
                products = cursor.fetchall()

            for i, (pid, name, stock) in enumerate(products):
                listbox.insert(tk.END, f"{pid}: {name} ({stock})")
                product_id_map[i] = (pid, name, stock)

        def adjust_stock(delta):
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a product.")
                return

            idx = selection[0]
            product_id, name, stock = product_id_map[idx]
            new_stock = stock + delta

            if new_stock < 0:
                messagebox.showerror("Error", "Stock cannot be negative.")
                return

            try:
                db = db_management()
                db.adjust_stock(self.user["id"], product_id, delta)
                load_products()  # Refresh list
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        button_frame = tk.Frame(win)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Increase (+1)", width=15, command=lambda: adjust_stock(+1)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Decrease (-1)", width=15, command=lambda: adjust_stock(-1)).grid(row=0, column=1, padx=5)

        load_products()

    def update_price_window(self):
        win = tk.Toplevel(self.root)
        win.title("Update price")

        tk.Label(win, text="Select a product to update:").pack(pady=5)

        listbox = tk.Listbox(win, width=40, height=10)
        listbox.pack(padx=10, pady=5)

        product_id_map = {}
        def load_products():
            listbox.delete(0, tk.END)
            product_id_map.clear()

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, price FROM products WHERE is_removed = 0")
                products = cursor.fetchall()

            for i, (pid, name, price) in enumerate(products):
                listbox.insert(tk.END, f"{pid}: {name} (${price})")
                product_id_map[i] = (pid, name, price)

        def confirm_update(win, entry, product_id, name):
            db = db_management()
            new_price = entry.get().strip() 
            try:
                try:
                    price = float(new_price)
                    if price < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Input Error", "Price must be a positive number.")
                    return

                db.update_price(self.user["id"], product_id, new_price)
                messagebox.showinfo("Updated", f"Product {name} updated successfully.")
                win.destroy()
                load_products()  # refresh listbox in-place
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        def initiate_update():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a product to update.")
                return

            idx = selection[0]
            product_id, name, price = product_id_map[idx]

            win2 = tk.Toplevel(win)
            win2.title("Update Price Info")

            tk.Label(win2, text=f"Product: {name}").grid(row=0, column=0, columnspan=2, pady=5)
            tk.Label(win2, text=f"Current price: ${price}").grid(row=1, column=0, columnspan=2, pady=5)
            tk.Label(win2, text="New price:").grid(row=2, column=0, pady=5)
            entry = tk.Entry(win2)
            entry.grid(row=2, column=1, pady=5)

            tk.Button(win2, text="Update", command=lambda:confirm_update(win2, entry, product_id, name)).grid(row=3, columnspan=2, pady=5)

        tk.Button(win, text="Update Selected Product", command=initiate_update).pack(pady=10)
        load_products()

    def stadistics_window():
        pass
    def view_products_window(self):
        win = tk.Toplevel(self.root)
        win.title("View products")

        columns = ("id", "name", "stock", "price")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, stretch=True)
        tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def load_data():
            # Query data
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, stock, price FROM products WHERE is_removed=0")
            records = cursor.fetchall()
            conn.close()

            # Clear table
            for row in tree.get_children():
                tree.delete(row)

            # Apply filters (search, user_id, action_type)
            for row in records:
                tree.insert("", tk.END, values=row)
        
        load_data()

    def open_activity_log_viewer(self):
        log_win = tk.Toplevel(self.root)
        log_win.geometry("1200x500")
        ActivityLogViewer(log_win)