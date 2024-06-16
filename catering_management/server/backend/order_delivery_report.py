# In backend/order_delivery_report.py
import tkinter as tk
from tkinter import ttk
import time
from backend.save_data import SaveData

class OrderDeliveryReport(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Order Delivery Time Report")
        self.geometry("600x400")
        self.configure(bg="#1F2836")

        self.orders = SaveData.load_orders()
        self.create_widgets()

    def create_widgets(self):
        columns = ("Order ID", "Customer Name", "Order Date", "Delivery Time", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.populate_data()

    def populate_data(self):
        # Separate and sort orders by status
        in_progress_orders = []
        delivered_orders = []

        current_time = time.time()

        for order in self.orders:
            # Calculate remaining time and status
            elapsed_time = (current_time - order['start_time']) / 60  # Convert to minutes
            remaining_time = max(order['prep_time'] - elapsed_time, 0)
            status = "Delivered" if remaining_time == 0 else "In Progress"
            delivery_time = f"{remaining_time:.2f} minutes" if remaining_time > 0 else f"{order['prep_time']} minutes"
            
            order_data = (
                order.get("transaction_id", ""),
                f"{order.get('first_name', '')} {order.get('last_name', '')}",
                time.strftime("%Y-%m-%d", time.localtime(order.get("start_time", 0))),
                delivery_time,
                status
            )
            
            if status == "In Progress":
                in_progress_orders.append(order_data)
            else:
                delivered_orders.append(order_data)

        # Insert In Progress orders first, then Delivered orders
        for order_data in in_progress_orders + delivered_orders:
            self.tree.insert("", tk.END, values=order_data)
