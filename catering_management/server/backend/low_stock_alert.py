import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
import json

class LowStockAlert:
    warehouse_file = 'warehouse_data.json'
    minimum_stock_file = 'minimum_stock_levels.json'

    def __init__(self, warehouse_path='warehouse_data.json', minimum_stock_path='minimum_stock_levels.json'):
        self.warehouse_path = warehouse_path
        self.minimum_stock_path = minimum_stock_path
        self.warehouse = self.load_warehouse_data()
        self.minimum_stock_levels = self.load_minimum_stock_levels()

    @staticmethod
    def load_warehouse_data():
        if os.path.exists(LowStockAlert.warehouse_file):
            with open(LowStockAlert.warehouse_file, 'r') as file:
                return json.load(file)
        return []

    @staticmethod
    def load_minimum_stock_levels():
        if os.path.exists(LowStockAlert.minimum_stock_file):
            with open(LowStockAlert.minimum_stock_file, 'r') as file:
                return json.load(file)
        return {}

    def print_low_stock_alert(self):
        warehouse_data = LowStockAlert.load_warehouse_data()
        minimum_stock_levels = LowStockAlert.load_minimum_stock_levels()

        low_stock_items = []
        for item in warehouse_data:
            item_name = item['name']
            current_quantity = int(item['quantity'])
            minimum_quantity = minimum_stock_levels.get(item_name, 0)
            if current_quantity < minimum_quantity:
                low_stock_items.append((item_name, current_quantity, minimum_quantity))

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Low Stock Alert Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(60, 10, txt="Item Name", align='L', fill=True)
        pdf.cell(40, 10, txt="Current Quantity", align='C', fill=True)
        pdf.cell(40, 10, txt="Minimum Quantity", align='R', fill=True)
        pdf.ln(10)

        for index, (item_name, current_quantity, minimum_quantity) in enumerate(low_stock_items, start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(60, 10, txt=item_name, align='L')
            pdf.cell(40, 10, txt=str(current_quantity), align='C')
            pdf.cell(40, 10, txt=str(minimum_quantity), align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'low_stock_alert_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")

