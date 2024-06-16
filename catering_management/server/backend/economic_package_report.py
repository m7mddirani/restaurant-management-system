import tkinter as tk
from tkinter import ttk
from backend.save_data import SaveData

class EconomicPackageReport(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Economic Package Report")
        self.geometry("600x400")
        self.configure(bg="#1F2836")

        self.orders = SaveData.load_orders()
        self.create_widgets()

    def create_widgets(self):
        columns = ("Package Name", "Times Ordered", "Total Revenue")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.populate_data()

    def populate_data(self):
        package_data = self.aggregate_package_data()
        for package in package_data:
            self.tree.insert("", tk.END, values=(
                package["name"],
                package["times_ordered"],
                f"{package['total_revenue']}"
            ))

    def aggregate_package_data(self):
        packages = ["Burger Economic Package", "Burger Family Package"]
        package_data = {pkg: {"times_ordered": 0, "total_revenue": 0} for pkg in packages}

        for order in self.orders:
            for item, qty in order["order"].items():
                if item in package_data:
                    package_data[item]["times_ordered"] += qty
                    package_data[item]["total_revenue"] += SaveData.get_item_price(item) * qty

        return [{"name": name, **data} for name, data in package_data.items()]

