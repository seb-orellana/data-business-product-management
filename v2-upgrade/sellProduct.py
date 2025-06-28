import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH
from db_utils import db_management

class SellProductsWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.selected_products = {}  # key: product_id, value: [name, quantity, price]

        self.win = tk.Toplevel(self.root)
        self.win.title("Sell Products")
        self.win.geometry("1000x500")

        tk.Label(self.win, text="Available Products").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.win, text="Current Sale").grid(row=0, column=2, padx=10, pady=5)

        self.product_listbox = tk.Listbox(self.win, width=40, height=20)
        self.product_listbox.grid(row=1, column=0, rowspan=4, padx=10, pady=5)
        self.product_id_map = {}

        tk.Label(self.win, text="Quantity").grid(row=1, column=1)
        self.qty_entry = tk.Entry(self.win, width=5)
        self.qty_entry.grid(row=2, column=1)

        tk.Button(self.win, text="Add", command=self.add_to_sale).grid(row=3, column=1, pady=5)

        # Treeview for current sale
        self.columns = ("id", "Name", "Qty", "Price", "Subtotal")
        self.tree = ttk.Treeview(self.win, columns=self.columns, show="headings", height=15)
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.grid(row=1, column=2, rowspan=4, padx=10)

        self.total_label = tk.Label(self.win, text="Total: $0")
        self.total_label.grid(row=5, column=2, pady=10)

        tk.Button(self.win, text="Remove Selected", command=self.remove_from_sale).grid(row=5, column=0)
        tk.Button(self.win, text="Confirm Sale", command=self.confirm_sale).grid(row=5, column=1)

        self.load_products()

    def load_products(self):
        self.product_listbox.delete(0, tk.END)
        self.product_id_map.clear()

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, stock, price FROM products WHERE is_removed = 0")
            products = cursor.fetchall()

        for i, (pid, name, stock, price) in enumerate(products):
            self.product_listbox.insert(tk.END, f"{name} | Stock: {stock} | ${price}")
            self.product_id_map[i] = (pid, name, stock, price)

    def add_to_sale(self):
        try:
            selection = self.product_listbox.curselection()
            if not selection:
                return messagebox.showwarning("Warning", "Select a product first.")

            idx = selection[0]
            product_id, name, stock, price = self.product_id_map[idx]
            qty = int(self.qty_entry.get())

            if qty <= 0:
                raise ValueError
            if qty > stock:
                return messagebox.showerror("Error", "Not enough stock.")

            if product_id in self.selected_products:
                new_qty = self.selected_products[product_id][1] + qty
                if new_qty > stock:
                    return messagebox.showerror("Error", "Not enough stock.")
                else:
                    self.selected_products[product_id][1] += qty
            else:
                self.selected_products[product_id] = [name, qty, price]

            self.refresh_tree()
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a positive integer.")

    def remove_from_sale(self):
        selection = self.tree.selection()
        if not selection:
            return messagebox.showwarning("Warning", "Select an item to remove.")

        for sel in selection:
            values = self.tree.item(sel, 'values')
            product_id = int(values[0])
            self.selected_products.pop(product_id, None)

        self.refresh_tree()

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0
        for pid, (name, qty, price) in self.selected_products.items():
            subtotal = qty * price
            total += subtotal
            self.tree.insert("", tk.END, values=(pid, name, qty, price, subtotal))

        self.total_label.config(text=f"Total: ${total}")

    def confirm_sale(self):
        if not self.selected_products:
            return messagebox.showwarning("Warning", "No products selected.")

        try:
            db = db_management()
            items = [{"product_id": pid, "quantity": qty} for pid, (_, qty, _) in self.selected_products.items()]
            db.sell_products(self.user["id"], items)
            messagebox.showinfo("Success", "Sale completed successfully.")
            self.win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Sale failed: {e}")
