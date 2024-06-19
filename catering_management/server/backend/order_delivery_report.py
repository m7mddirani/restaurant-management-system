import time
import tkinter as tk


from tkinter import ttk

from backend.save_data import SaveData

class OrderDeliveryReport(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Order Delivery Time Report")
        self.geometry("600x400")
        self.configure(bg="#1F2836")

        self.create_widgets()
        self.reload_orders()

    def create_widgets(self):
        columns = ("Order ID", "Customer Name", "Order Date", "Delivery Time", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

    def reload_orders(self):
        self.orders = SaveData.load_orders()
        self.populate_data()

    def populate_data(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing data

        in_progress_orders = []
        delivered_orders = []

        current_time = time.time()

        for order in self.orders:
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

        for order_data in in_progress_orders + delivered_orders:
            self.tree.insert("", tk.END, values=order_data)