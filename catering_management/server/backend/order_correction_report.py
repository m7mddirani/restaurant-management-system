import tkinter as tk


from tkinter import ttk

from backend.save_data import SaveData

class OrderCorrectionReport(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Order Correction Report")
        self.geometry("600x400")
        self.configure(bg="#1F2836")

        self.order_corrections = SaveData.load_order_corrections()
        self.create_widgets()

    def create_widgets(self):
        columns = ("Order ID", "Customer Name", "Order Date", "Modification Date", "Changes Made")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.populate_data()

    def populate_data(self):
        for correction in self.order_corrections:
            self.tree.insert("", tk.END, values=(
                correction.get("transaction_id", ""),
                correction.get("customer_name", ""),
                correction.get("original_order_date", ""),
                correction.get("modification_date", ""),
                correction.get("changes_made", "")
            ))
