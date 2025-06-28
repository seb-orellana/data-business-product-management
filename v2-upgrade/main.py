from db_utils import db_management
from GUI import BusinessGUI
from loginGUI import LoginFrame
import tkinter as tk

def start_gui(id, username, role):
    BusinessGUI(root, id, username, role)

if __name__ == '__main__':
    db = db_management()
    root = tk.Tk()
    root.title("Login")
    LoginFrame(root, start_gui)
    root.mainloop()
