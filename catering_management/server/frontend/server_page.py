import tkinter as tk
from backend.save_data import SaveData
from backend.warehouse import Warehouse
from backend.menu_page import MenuPage
from backend.orders_page import OrdersPage
from backend.warehouse_page import WarehousePage
from backend.reports_page import ReportsPage  
from backend.valuable_customer import CustomerReport

# server_page.py
class ServerPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#1F2836")
        self.orders = SaveData.load_orders()  # Load orders from JSON file
        self.warehouse = Warehouse()  # Initialize warehouse

        # Create sidebar    
        self.sidebar = tk.Frame(self, bg="#2C3E50", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.create_sidebar()

        # Create main content area
        self.content = tk.Frame(self, bg="#1F2836")
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.show_menu_page()

    def create_sidebar(self):
        # Sidebar user info
        user_frame = tk.Frame(self.sidebar, bg="#34495E", height=100)
        user_frame.pack(fill=tk.X)
        user_label = tk.Label(user_frame, text="Khosravi", bg="#34495E", fg="white", font=("Arial", 14))
        user_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Sidebar buttons
        menu_button = tk.Button(self.sidebar, text="Menu", bg="#2C3E50", fg="white", command=self.show_menu_page, bd=0, font=("Arial", 12))
        menu_button.pack(fill=tk.X, pady=5)
        orders_button = tk.Button(self.sidebar, text="Orders", bg="#2C3E50", fg="white", command=self.show_orders_page, bd=0, font=("Arial", 12))
        orders_button.pack(fill=tk.X, pady=5)
        warehouse_button = tk.Button(self.sidebar, text="Warehouse", bg="#2C3E50", fg="white", command=self.show_warehouse_page, bd=0, font=("Arial", 12))
        warehouse_button.pack(fill=tk.X, pady=5)
        reports_button = tk.Button(self.sidebar, text="Reports", bg="#2C3E50", fg="white", command=self.show_reports_page, bd=0, font=("Arial", 12))
        reports_button.pack(fill=tk.X, pady=5)

    def show_menu_page(self, order_to_edit=None):
        print("Showing menu page")  # Debugging statement
        self.clear_content()
        menu_page = MenuPage(self.content, self, self.orders, order_to_edit=order_to_edit, on_save=self.show_orders_page)
        menu_page.pack(fill=tk.BOTH, expand=True)
        print("Menu page should be displayed now")  # Debugging statement

    def show_orders_page(self):
        print("Showing orders page")  # Debugging statement
        self.clear_content()
        orders = SaveData.load_orders()  # Load orders from JSON file
        orders_page = OrdersPage(self.content, self, orders)
        orders_page.pack(fill=tk.BOTH, expand=True)

    def show_warehouse_page(self):
        print("Showing warehouse page")  # Debugging statement
        self.clear_content()
        warehouse_page = WarehousePage(self.content, self.warehouse)
        warehouse_page.pack(fill=tk.BOTH, expand=True)

    def show_reports_page(self):
        print("Showing reports page")  # Debugging statement
        self.clear_content()
        reports_page = ReportsPage(self.content)
        customer_report = CustomerReport(self.content)
        reports_page.pack(fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def add_order(self, order_data):
        print(f"Adding order: {order_data}")  # Debugging statement
        self.orders.append(order_data)
        SaveData.save_orders(self.orders)  # Save all orders at once
        SaveData.save_order_time(order_data["transaction_id"], order_data["start_time"])
        self.show_orders_page()

    def update_order(self, updated_order):
        for i, order in enumerate(self.orders):
            if order['transaction_id'] == updated_order['transaction_id']:
                self.orders[i] = updated_order
                break
        SaveData.save_orders(self.orders)  # Save the updated orders list
        self.show_orders_page()
