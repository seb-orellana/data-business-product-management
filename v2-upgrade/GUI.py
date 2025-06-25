import tkinter as tk
from tkinter import messagebox
from config import DB_PATH
import sqlite3

CURRENT_USER = {
    "id": 1,
    "username": "admin",
    "role": "admin"  # or "employee"
}

class StoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Management")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.build_interface()

    def build_interface(self):
        tk.Label(self.main_frame, text=f"Logged in as: {CURRENT_USER['username']} ({CURRENT_USER['role']})").grid(row=0, column=0, columnspan=2)

        # Admin-only features
        if CURRENT_USER['role'] == 'admin':
            tk.Button(self.main_frame, text="Create User", command=self.create_user_window).grid(row=1, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Delete User", command=self.delete_user_window).grid(row=2, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Add Product", command=self.add_product_window).grid(row=3, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Remove Product", command=self.remove_product_window).grid(row=4, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Update Stock", command=self.update_stock_window).grid(row=5, column=0, sticky='ew')
            tk.Button(self.main_frame, text="Update Price", command=self.update_price_window).grid(row=6, column=0, sticky='ew')

        # Common features
        tk.Button(self.main_frame, text="Sell Products", command=self.sell_products_window).grid(row=7, column=0, sticky='ew')
        tk.Button(self.main_frame, text="Adjust Stock", command=self.adjust_stock_window).grid(row=8, column=0, sticky='ew')

    def create_user_window(self):
        self.simple_form_window("Create User", ["Username", "Password", "Role"], self.create_user_db)

    def delete_user_window(self):
        #show non deleted users, excluding itself
        #select user
        #confirm
        pass

    def add_product_window(self):
        self.simple_form_window("Add Product", ["Name", "Price", "Stock"], self.add_product_db)

    def remove_product_window(self):
        #show non removed products
        #select product
        #confirm
        pass

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

    # Placeholder DB functions
    def create_user_db(self, data):
        messagebox.showinfo("Info", f"User {data['Username']} created (simulated)")

    def delete_user_db(self, data):
        messagebox.showinfo("Info", f"User {data['Username']} deleted (simulated)")

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
