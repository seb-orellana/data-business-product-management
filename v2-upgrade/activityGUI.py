import tkinter as tk
from tkinter import ttk
import sqlite3

DB_PATH = "v2-upgrade/store.db"

class ActivityLogViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Log Viewer")

        # ===== Filters Frame =====
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        # Search term
        self.search_var = tk.StringVar()
        tk.Label(filter_frame, text="Search:").grid(row=0, column=0)
        tk.Entry(filter_frame, textvariable=self.search_var, width=20).grid(row=0, column=1)

        # User ID filter
        self.user_id_var = tk.StringVar()
        tk.Label(filter_frame, text="User ID:").grid(row=0, column=2)
        tk.Entry(filter_frame, textvariable=self.user_id_var, width=10).grid(row=0, column=3)

        # Action Type filter with Combobox
        self.action_type_var = tk.StringVar()
        tk.Label(filter_frame, text="Action Type:").grid(row=0, column=4)

        self.action_type_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.action_type_var,
            values=["All", "create_users", "delete_user", "add_product", "remove_product",
                    "sell_products", "update_stock", "adjust_stock", "update_price"],
            state="readonly",
            width=18
        )
        self.action_type_combo.current(0)  # Default to "All"
        self.action_type_combo.grid(row=0, column=5)

        # Apply filter button
        tk.Button(filter_frame, text="Apply Filters", command=self.load_data).grid(row=0, column=6, padx=10)

        # ===== Treeview Table =====
        columns = ("id", "user_id", "action_type", "action", "timestamp")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title(), command=lambda c=col: self.sort_by(c, False))
            self.tree.column(col, anchor=tk.CENTER, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

    def load_data(self):
        # Read filters
        search_term = self.search_var.get().lower()
        user_id_filter = self.user_id_var.get().strip()
        action_type_filter = self.action_type_var.get().strip().lower()

        # Query data
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, action_type, action, timestamp FROM activity_log ORDER BY id DESC")
        records = cursor.fetchall()
        conn.close()

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Apply filters (search, user_id, action_type)
        for row in records:
            id_, uid, atype, action, timestamp = row
            if (search_term in str(row).lower() and
                (not user_id_filter or str(uid) == user_id_filter) and
                (action_type_filter == "all" or (atype and atype.lower() == action_type_filter))):
                self.tree.insert("", tk.END, values=row)

    def sort_by(self, col, reverse):
        # Get all values
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)

        # Reorder rows
        for index, (val, k) in enumerate(l):
            self.tree.move(k, "", index)

        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.sort_by(col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityLogViewer(root)
    root.geometry("1200x500")
    root.mainloop()
