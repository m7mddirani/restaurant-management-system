import json
import os
import random
import time

class SaveData:
    _order = []
    customer_codes_file = 'customer_codes.json'
    orders_file = 'orders.json'
    warehouse_file = 'warehouse_data.json'
    order_times_file = 'order_times.json'

    def __init__(self, customer_codes_file_path='customer_codes.json', orders_file_path='orders.json', warehouse_path ='warehouse_data.json', order_times_file_path='order_times.json'):
        self.customer_codes_file = customer_codes_file_path
        self.customer_codes = self.load_customer_codes()
        self.orders_file_path = orders_file_path
        self.orders = self.load_orders()
        self.warehouse_path = warehouse_path
        self.warehouse = self.load_warehouse_data()
        self.order_times_file_path = order_times_file_path
        self.order_times = self.load_order_times()

    @staticmethod
    def add_item(item_name):
        SaveData._order.append(item_name)

    @staticmethod
    def get_order():
        return SaveData._order

    @staticmethod
    def reset_order():
        SaveData._order = []

    @staticmethod
    def get_menu_groups():
        return {
            "Traditional Food": [
                {"name": "Kabab", "price": 40000, "prep_time": 10, "image": "kabab.png"},
                {"name": "Joje", "price": 45000, "prep_time": 10, "image": "joje.png"},
                {"name": "Barg", "price": 50000, "prep_time": 15, "image": "barg.png"},
                {"name": "Tahchin", "price": 35000, "prep_time": 30, "image": "tahchin.png"},
                {"name": "Rice", "price": 25000, "prep_time": 15, "image": "rice.png"},
                {"name": "Salad", "price": 35000, "prep_time": 8, "image": "salad.png"},
            ],
            "Chicken Strips": [
                {"name": "Chicken Strips 2", "price": 120000, "prep_time": 15, "image": "chicken_strips_2.png"},
                {"name": "Chicken Strips 3", "price": 135000, "prep_time": 15, "image": "chicken_strips_3.png"},
                {"name": "Chicken Strips 4", "price": 160000, "prep_time": 15, "image": "chicken_strips_4.png"},
                {"name": "Chicken Strips 5", "price": 180000, "prep_time": 15, "image": "chicken_strips_5.png"},
            ],
            "Burgers": [
                {"name": "American Burger", "price": 150000, "prep_time": 10, "image": "american_burger.png"},
                {"name": "Burger Economic Package", "price": 185000, "prep_time": 25, "image": "burger_small_package.png"},
                {"name": "Burger Family Package", "price": 300000, "prep_time": 35, "image": "burger_family_package.png"},
                {"name": "Chicken Burger", "price": 135000, "prep_time": 10, "image": "chicken_burger.png"},
            ],
            "Potatoes": [
                {"name": "Potato Large Box", "price": 15000, "prep_time": 5, "image": "potato_large_box.png"},
                {"name": "Potato Small Box", "price": 8000, "prep_time": 5, "image": "potato_small_box.png"},
            ],
            "Drinks": [
                {"name": "Pepsi", "price": 10000, "prep_time": 1, "image": "pepsi.png"},
                {"name": "Doogh", "price": 8000, "prep_time": 1, "image": "doogh.png"},
            ]
        }

    @staticmethod
    def get_item_price(item_name):
        for group in SaveData.get_menu_groups().values():
            for item in group:
                if item["name"] == item_name:
                    return item["price"]
        return 0

    @staticmethod
    def get_item_prep_time(item_name):
        for group in SaveData.get_menu_groups().values():
            for item in group:
                if item["name"] == item_name:
                    return item["prep_time"]
        return 0

    @staticmethod
    def load_customer_codes():
        if os.path.exists(SaveData.customer_codes_file):
            with open(SaveData.customer_codes_file, 'r') as file:
                return json.load(file)
        return {}

    @staticmethod
    def save_customer_codes(codes):
        with open(SaveData.customer_codes_file, 'w') as file:
            json.dump(codes, file, indent=4)

    @staticmethod
    def get_or_generate_code(first_name, last_name):
        codes = SaveData.load_customer_codes()
        new_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        while new_code in codes:
            new_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        codes[new_code] = {"uses": 1, "discount": 0, "first_name": first_name, "last_name": last_name}
        SaveData.save_customer_codes(codes)
        return {"code": new_code, "discount": 0, "first_name": first_name, "last_name": last_name}

    @staticmethod
    def increment_code_usage(code):
        codes = SaveData.load_customer_codes()
        if code in codes:
            codes[code]["uses"] += 1
            if codes[code]["uses"] > 20:
                codes[code]["discount"] = 20
            elif codes[code]["uses"] > 10:
                codes[code]["discount"] = 10
            SaveData.save_customer_codes(codes)
            return {"code": code, "discount": codes[code]["discount"], "uses": codes[code]["uses"]}
        return None

    @staticmethod
    def apply_discount(total_price, discount):
        return total_price * (1 - discount / 100)
        

    @staticmethod
    def save_order_time(transaction_id, start_time):
        order_times = SaveData.load_order_times()
        human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        order_times.append({"transaction_id": transaction_id, "start_time": human_readable_time})
        with open(SaveData.order_times_file, 'w') as file:
            json.dump(order_times, file, indent=4)

    @staticmethod
    def save_orders(orders):
        with open(SaveData.orders_file, 'w') as file:
            json.dump(orders, file, indent=4)

    @staticmethod
    def load_orders():
        if os.path.exists(SaveData.orders_file):
            with open(SaveData.orders_file, 'r') as file:
                orders = json.load(file)
                # Ensure all orders are dictionaries
                return [order for order in orders if isinstance(order, dict)]
        return []


    @staticmethod
    def load_order_times():
        if os.path.exists(SaveData.order_times_file):
            with open(SaveData.order_times_file, 'r') as file:
                return json.load(file)
        return []
    
    @staticmethod
    def load_warehouse_data():
        if os.path.exists(SaveData.warehouse_file):
            with open(SaveData.warehouse_file, 'r') as file:
                return json.load(file)
        return []
    
    @staticmethod
    def save_warehouse_data(data):
        with open(SaveData.warehouse_file, 'w') as file:
            json.dump(data, file, indent=4)

