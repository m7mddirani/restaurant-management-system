import os


from fpdf import FPDF
from tkinter import messagebox

from backend.save_data import SaveData


class MostOrdered:
    orders_file = 'orders.json'

    def __init__(self, orders_file_path='orders.json'):
        self.orders_file_path = orders_file_path
        self.orders = self.load_orders()

    @staticmethod
    def load_orders():
        return SaveData.load_orders()

    @staticmethod
    def save_order(order):
        orders = SaveData.load_orders()
        orders.append(order)
        SaveData.save_orders(orders)

    def print_most_ordered_items(self):
        orders = SaveData.load_orders()
        item_counts = {}
        for order in orders:
            for item, count in order["order"].items():
                if item in item_counts:
                    item_counts[item] += count
                else:
                    item_counts[item] = count

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Most Ordered Items Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(80, 10, txt="Item Name", align='L', fill=True)
        pdf.cell(80, 10, txt="Number of Orders", align='R', fill=True)
        pdf.ln(10)

        for index, (item, count) in enumerate(sorted(item_counts.items(), key=lambda x: x[1], reverse=True), start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(80, 10, txt=item, align='L')
            pdf.cell(80, 10, txt=str(count), align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'most_ordered_items_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")
