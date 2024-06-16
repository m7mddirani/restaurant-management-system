import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
import json

class MaterialsQuantities(tk.Frame):
    warehouse_file = 'warehouse_data.json'

    def __init__(self, warehouse_path = 'warehouse_data.json'):
        self.warehouse_path = warehouse_path
        self.warehouse = self.load_warehouse_data()

    @staticmethod
    def load_warehouse_data():
        if os.path.exists(MaterialsQuantities.warehouse_file):
            with open(MaterialsQuantities.warehouse_file, 'r') as file:
                return json.load(file)
        return []


    def print_items_by_quantity(self):
        warehouse_data = MaterialsQuantities.load_warehouse_data()

        if isinstance(warehouse_data[0], list):
            warehouse_data = warehouse_data[0]

        for item in warehouse_data:
            item["quantity"] = int(item["quantity"])

        quantity_items = sorted(warehouse_data, key=lambda x: x["quantity"])

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Items by Quantity Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(60, 10, txt="Item Name", align='L', fill=True)
        pdf.cell(40, 10, txt="Quantity", align='C', fill=True)
        pdf.cell(40, 10, txt="Unit", align='R', fill=True)
        pdf.ln(10)

        for index, item in enumerate(quantity_items, start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(60, 10, txt=item["name"], align='L')
            pdf.cell(40, 10, txt=str(item["quantity"]), align='C')
            pdf.cell(40, 10, txt=item["unit"], align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..','..','reports', 'items_by_quantity_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")
