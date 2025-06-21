from db_utils import db_management

def main():
    db = db_management()
    db.create_users("userTest", "pwsdTest", "admin")
    db.add_product("productTest", 1000, 10)
    db.add_product("productTest2", 3000, 50)
    db.add_product("productTest3", 5000, 32)
    
    sale = [{"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 10},
            {"product_id": 3, "quantity": 1}]
    
    db.sell_products(1, sale)

if __name__ == '__main__':
    main()
