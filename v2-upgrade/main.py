from db_utils import db_management
from GUI import BusinessGUI
from loginGUI import LoginFrame
import tkinter as tk

from config import DB_PATH, admin_user, admin_pass

def main():
    db = db_management()
 
    sale = [{"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 10},
            {"product_id": 3, "quantity": 1}]
    
    db.sell_products(2, sale)
    db.change_password(1, "userTest", "hello123")

def start_gui(id, username, role):
    BusinessGUI(root, id, username, role)

if __name__ == '__main__':
    #main()
    db = db_management()
    root = tk.Tk()
    root.title("Login")
    LoginFrame(root, start_gui)
    root.mainloop()
