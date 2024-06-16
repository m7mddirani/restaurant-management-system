import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
import json
import time
from backend.save_data import SaveData
class Earnings:

    menu_file = 'menu.json'

    def __init__(self, menu_file_path='menu.json'):
        self.menu_file_path = menu_file_path
        self.menu_file = self.load_menu()

    @staticmethod
    def load_menu():
        menu_file = 'menu.json'
        if os.path.exists(menu_file):
            with open(menu_file, 'r') as file:
                return json.load(file)[0]
        return {}

    @staticmethod
    def get_production_price(item_name):
        menu_data = Earnings.load_menu()
        for category in menu_data.values():
            for item in category:
                if item["name"] == item_name:
                    return item["Production Price"]
        return 0

    @staticmethod
    def get_sale_price(item_name):
        menu_data = Earnings.load_menu()
        for category in menu_data.values():
            for item in category:
                if item["name"] == item_name:
                    return item["Sale Price"]
        return 0

    @staticmethod
    def load_orders():
        return SaveData.load_orders()

    def print_earnings_report(self):
        selected_date = self.date_entry.get_date().strftime("%Y-%m-%d")
        filtered_orders = [
            order for order in SaveData.load_orders()
            if time.strftime("%Y-%m-%d", time.localtime(order['start_time'])) == selected_date
        ]

        total_earnings = 0
        net_earnings = 0

        for order in filtered_orders:
            for item, quantity in order['order'].items():
                sale_price = Earnings.get_sale_price(item)
                production_price = Earnings.get_production_price(item)
                total_earnings += sale_price * quantity
                net_earnings += (sale_price - production_price) * quantity

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Earnings Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(80, 10, txt=f"Date: {selected_date}", align='L', fill=True)
        pdf.cell(60, 10, txt=f"Total Earnings: {total_earnings}", align='C', fill=True)
        pdf.cell(60, 10, txt=f"Net Earnings: {net_earnings}", align='R', fill=True)
        pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'earnings_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Earnings report has been printed to {pdf_output_path}")
