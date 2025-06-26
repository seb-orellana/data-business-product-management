import tkinter as tk
from tkinter import messagebox, ttk
from config import DB_PATH
import sqlite3
from db_utils import db_management

CURRENT_USER = {
    "id": 1,
    "username": "admin",
    "role": "admin"  #admin or manager or employee
}

class StoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x400")
        self.root.title("Business Management")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=15, pady=15)

        self.build_interface()

    def build_interface(self):
        tk.Label(self.main_frame, text=f"Logged in as: {CURRENT_USER['username']} ({CURRENT_USER['role']})").grid(row=0, column=0, columnspan=2)

        # Admin-only features
        if CURRENT_USER['role'] == 'admin':
            tk.Button(self.main_frame, text="Create User", command=self.create_user_window).grid(row=1, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Delete User", command=self.delete_user_window).grid(row=2, column=0, sticky='ew')

        if CURRENT_USER['role'] == 'admin' or CURRENT_USER['role'] == 'manager':
            tk.Button(self.main_frame, text="Add Product", command=self.add_product_window).grid(row=3, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Remove Product", command=self.remove_product_window).grid(row=4, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Update Stock", command=self.update_stock_window).grid(row=5, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Update Price", command=self.update_price_window).grid(row=6, column=0, sticky='ew')

        # Common features
        tk.Button(self.main_frame, text="Sell Products", command=self.sell_products_window).grid(row=7, column=0, sticky='ew')
        tk.Button(self.main_frame, text="Adjust Stock", command=self.adjust_stock_window).grid(row=8, column=0, sticky='ew')

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
                db.create_users(CURRENT_USER["id"], data["Username"], data["Password"], role.get())
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
                db.delete_user(CURRENT_USER["id"], user_id)
                messagebox.showinfo("Deleted", f"User {username} deleted successfully.")
                load_users()  # refresh listbox in-place
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(win, text="Delete Selected User", command=confirm_deletion).pack(pady=10)
        load_users()

    def add_product_window(self):
        self.simple_form_window("Add Product", ["Name", "Price", "Stock"], self.add_product_db)

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
                messagebox.showwarning("Warning", "Please select a product to delete.")
                return

            idx = selection[0]
            product_id, name = product_id_map[idx]
            
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the product: {name}?")
            if not confirm:
                return

            try:
                db.remove_product(CURRENT_USER["id"], product_id)
                messagebox.showinfo("Deleted", f"Product {name} deleted successfully.")
                load_products()  # refresh listbox in-place
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(win, text="Delete Selected Product", command=confirm_deletion).pack(pady=10)
        load_products()

    def sell_products_window(self):
        pass

    def update_stock_window(self):
        #show non removed products
        #select product
        #type new stock
        #confirm
        pass

    def adjust_stock_window(self):
        #show non removed products
        #select product
        #choose add or remove
        #type number
        #confirm
        pass

    def update_price_window(self):
        #show non removed products
        #select product
        #type number
        #confirm
        pass

    def simple_form_window(self, title, fields, callback):
        win = tk.Toplevel(self.root)
        win.title(title)
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(win, text=field).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[field] = entry

        def submit():
            data = {field: entries[field].get() for field in fields}
            callback(data)
            win.destroy()

        tk.Button(win, text="Submit", command=submit).grid(row=len(fields), columnspan=2)

    def add_product_db(self, data):
        messagebox.showinfo("Info", f"Product {data['Name']} added (simulated)")

    def remove_product_db(self, data):
        messagebox.showinfo("Info", f"Product {data['Product ID']} removed (simulated)")

    def sell_product_db(self, data):
        messagebox.showinfo("Info", f"Sold {data['Quantity']} of product {data['Product ID']} (simulated)")

    def update_stock_db(self, data):
        messagebox.showinfo("Info", f"Stock for product {data['Product ID']} updated to {data['New Stock']} (simulated)")

    def adjust_stock_db(self, data):
        messagebox.showinfo("Info", f"Stock for product {data['Product ID']} adjusted by {data['Change (+/-)']} (simulated)")

    def update_price_db(self, data):
        messagebox.showinfo("Info", f"Price for product {data['Product ID']} updated to {data['New Price']} (simulated)")

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreGUI(root)
    root.mainloop()
