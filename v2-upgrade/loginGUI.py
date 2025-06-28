import tkinter as tk
import sqlite3
from db_utils import db_management  # or adjust to your actual import
from tkinter import messagebox
from config import DB_PATH

class LoginFrame(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.master = master
        self.on_success = on_success  # callback when login is successful

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Username:").grid(row=0, column=0, pady=5)
        tk.Entry(self, textvariable=self.username_var).grid(row=0, column=1, pady=5)

        tk.Label(self, text="Password:").grid(row=1, column=0, pady=5)
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)

        tk.Button(self, text="Login", command=self.attempt_login).grid(row=2, column=0, columnspan=2, pady=10)

        self.pack(padx=20, pady=20)

    def attempt_login(self):
        db = db_management()

        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
            
                cursor.execute("SELECT id, role FROM users WHERE is_deleted=0 AND username=?", (username,))
                result = cursor.fetchone()
                conn.commit()

            if result == None:
                messagebox.showerror("Login Failed", "Invalid username.")
            else:
                log_in = db.log_in(username, password)
                
                if log_in:
                    self.destroy()
                    self.on_success(result[0], username, result[1])  # callback to launch StoreGUI
                else:
                    messagebox.showerror("Login Failed", "Invalid password.")

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database Error", f"Integrity error: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")



