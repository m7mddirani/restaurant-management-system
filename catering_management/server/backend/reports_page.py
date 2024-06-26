import os
import tkinter as tk


from PIL import Image, ImageTk
from tkcalendar import DateEntry

from backend.most_visited_times import VisitedTimes
from backend.valuable_customer import CustomerReport
from backend.earnings import Earnings
from backend.most_ordered import MostOrdered
from backend.expiration_dates import ExpirationDates
from backend.materials_quantities import MaterialsQuantities
from backend.customer_history import CustomerHistory
from backend.order_delivery_report import OrderDeliveryReport
from backend.order_correction_report import OrderCorrectionReport
from backend.economic_package_report import EconomicPackageReport
from backend.low_stock_alert import LowStockAlert
from backend.stock_aging_report import StockAgingReport
from backend.turnover_report import WarehouseTurnoverReport



class ReportsPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#dbd7cd")
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_reports_frame()

    def create_reports_frame(self):

        date_label = tk.Label( text="Select Date:", bg="#dbd7cd", fg="#334e41", font=("Arial", 12))
        date_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.date_entry = DateEntry( width=12, bg="#dbd7cd", fg="#334e41", borderwidth=2)
        self.date_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        buttons = [
            ("Print Valuable Customers", self.print_customers),
            ("Print Most Ordered Items", self.print_most_ordered_items),
            ("Print Most Visited Times", self.print_most_visited_times),
            ("Print Earnings Report", self.print_earnings_report),
            ("Print Nearest Expiration Dates", self.print_nearest_expiration_items),
            ("Print Items by Quantity", self.print_items_by_quantity),
            ("Print Customer History", self.show_customer_history_input),
            ("Order Delivery Time Report", self.show_order_delivery_report),
            ("Order Correction Report", self.show_order_correction_report),
            ("Economic Package Report", self.show_economic_package_report),
            ("Low Stock Alert Report", self.show_low_stock_alert_report),
            ("Stock Aging Report", self.show_stock_aging_report),
            ("Warehouse Turnover Report", self.show_warehouse_turnover_report)
        ]

        button_frame = tk.Frame(self) 
        button_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(button_frame, text=text, command=command, bg="#dbd7cd", fg="#334e41", font=("Arial", 12), width=30)
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    def show_economic_package_report(self):
        EconomicPackageReport(self)

    def show_order_correction_report(self):
        OrderCorrectionReport(self)

    def print_customers(self):
        CustomerReport.print_customers(self)

    def print_earnings_report(self):
        Earnings.print_earnings_report(self)

    def print_most_ordered_items(self):
        MostOrdered.print_most_ordered_items(self)

    def print_most_visited_times(self):
        VisitedTimes.print_most_visited_times(self)

    def print_nearest_expiration_items(self):
        ExpirationDates.print_nearest_expiration_items(self)

    def print_items_by_quantity(self):
        MaterialsQuantities.print_items_by_quantity(self)

    def show_order_delivery_report(self):
        OrderDeliveryReport(self)

    def show_low_stock_alert_report(self):
        LowStockAlert.print_low_stock_alert(self)

    def show_stock_aging_report(self):
        StockAgingReport.print_stock_aging_report(self)

    def print_customer_order_history(self, customer_name):
        CustomerHistory.print_customer_history(customer_name)

    def show_warehouse_turnover_report(self):
        WarehouseTurnoverReport.print_warehouse_turnover_report(self)

    def show_customer_history_input(self):
        input_window = tk.Toplevel(self)
        input_window.title("Customer Order History")
        input_window.geometry("400x200")
        input_window.configure(bg="#dbd7cd")

        tk.Label(input_window, text="Customer Name", bg="#dbd7cd", fg="#334e41").pack(pady=10)
        customer_name_entry = tk.Entry(input_window)
        customer_name_entry.pack(pady=10)

        tk.Button(input_window, text="Print", command=lambda: self.print_customer_order_history(customer_name_entry.get()), bg="#dbd7cd", fg="#334e41").pack(pady=10)
    def print_customer_order_history(self, customer_name):
        customer_order_history = CustomerHistory()
        customer_order_history.print_customer_history(customer_name)



