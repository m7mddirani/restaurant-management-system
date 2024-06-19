import os
import json


from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF


class StockAgingReport:
    warehouse_file = 'warehouse_data.json'

    def __init__(self, warehouse_path='warehouse_data.json'):
        self.warehouse_path = warehouse_path
        self.warehouse = self.load_warehouse_data()

    @staticmethod
    def load_warehouse_data():
        if os.path.exists(StockAgingReport.warehouse_file):
            with open(StockAgingReport.warehouse_file, 'r') as file:
                return json.load(file)
        return []

    def print_stock_aging_report(self):
        warehouse_data = StockAgingReport.load_warehouse_data()

        stock_aging_items = []
        current_date = datetime.now()

        for item in warehouse_data:
            entry_date = datetime.strptime(item["entry_date"], '%Y-%m-%d')
            days_in_stock = (current_date - entry_date).days
            stock_aging_items.append((item["name"], item["quantity"], days_in_stock))

        stock_aging_items.sort(key=lambda x: x[2], reverse=True)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Stock Aging Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(60, 10, txt="Item Name", align='L', fill=True)
        pdf.cell(40, 10, txt="Quantity", align='C', fill=True)
        pdf.cell(40, 10, txt="Days in Stock", align='R', fill=True)
        pdf.ln(10)

        for index, (item_name, quantity, days_in_stock) in enumerate(stock_aging_items, start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(60, 10, txt=item_name, align='L')
            pdf.cell(40, 10, txt=str(quantity), align='C')
            pdf.cell(40, 10, txt=str(days_in_stock), align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'stock_aging_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")