from db_utils import db_management

def main():
    db = db_management()
    db.create_users("userTest", "pwsdTest", "admin")

if __name__ == '__main__':
    main()
