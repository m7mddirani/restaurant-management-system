import os
import json


from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF


class WarehouseTurnoverReport:
    warehouse_file = 'warehouse_data.json'

    def __init__(self, warehouse_path='warehouse_data.json'):
        self.warehouse_path = warehouse_path
        self.warehouse = self.load_warehouse_data()

    @staticmethod
    def load_warehouse_data():
        if os.path.exists(WarehouseTurnoverReport.warehouse_file):
            with open(WarehouseTurnoverReport.warehouse_file, 'r') as file:
                return json.load(file)
        return []

    def print_warehouse_turnover_report(self):
        warehouse_data = WarehouseTurnoverReport.load_warehouse_data()

        turnover_items = []
        current_date = datetime.now()

        for item in warehouse_data:
            entry_date = datetime.strptime(item["entry_date"], '%Y-%m-%d')
            days_in_stock = (current_date - entry_date).days
            turnover_rate = int(item["quantity"]) / days_in_stock if days_in_stock > 0 else int(item["quantity"])
            turnover_items.append((item["name"], item["quantity"], days_in_stock, turnover_rate))

        turnover_items.sort(key=lambda x: x[3], reverse=True)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Warehouse Turnover Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(60, 10, txt="Item Name", align='L', fill=True)
        pdf.cell(30, 10, txt="Quantity", align='C', fill=True)
        pdf.cell(30, 10, txt="Days in Stock", align='C', fill=True)
        pdf.cell(30, 10, txt="Turnover Rate", align='R', fill=True)
        pdf.ln(10)

        for index, (item_name, quantity, days_in_stock, turnover_rate) in enumerate(turnover_items, start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(60, 10, txt=item_name, align='L')
            pdf.cell(30, 10, txt=str(quantity), align='C')
            pdf.cell(30, 10, txt=str(days_in_stock), align='C')
            pdf.cell(30, 10, txt=f"{turnover_rate:.2f}", align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'warehouse_turnover_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")
