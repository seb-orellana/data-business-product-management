from db_utils import db_management
from GUI import BusinessGUI
from loginGUI import LoginFrame
import tkinter as tk

from config import DB_PATH, admin_user, admin_pass

def main():
    db = db_management()

    db.create_users(1, "userTest", "pwsdTest", "manager")
    db.create_users(2, "userTest2", "Testpwsd", "employee")
    db.log_in("userTest", "adwds")
    db.log_in("userTest", "pwsdTest")
    db.add_product(1, "productTest", 1000, 10)
    db.add_product(1, "productTest2", 3000, 50)
    db.add_product(1, "productTest3", 5000, 32)
    
    sale = [{"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 10},
            {"product_id": 3, "quantity": 1}]
    
    db.sell_products(2, sale)

    db.update_stock(1, 1, 20)
    db.adjust_stock(2, 1, 3)
    db.update_price(1, 3, 3000)

    db.delete_user(1, 2)
    db.remove_product(1,2)
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
