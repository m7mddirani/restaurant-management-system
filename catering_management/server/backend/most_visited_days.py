import json
import os


from fpdf import FPDF
from tkinter import messagebox
from datetime import datetime

class VisitedDays:
    _order = []
    orders_file = 'orders.json'

    def __init__(self, orders_file_path='orders.json'):
        self.orders_file_path = orders_file_path
        self.orders = self.load_orders()

    @staticmethod
    def load_orders():
        if os.path.exists(VisitedDays.orders_file):
            with open(VisitedDays.orders_file, 'r') as file:
                return json.load(file)
        return []

    @staticmethod
    def extract_order_days_from_orders():
        orders = VisitedDays.load_orders()
        order_days = {}
        for order in orders:
            order_date = datetime.fromtimestamp(order[0]["start_time"] if isinstance(order, list) else order["start_time"]).strftime('%Y-%m-%d')
            if order_date in order_days:
                order_days[order_date] += 1
            else:
                order_days[order_date] = 1
        return order_days

    def print_most_visited_days(self):
        order_days = VisitedDays.extract_order_days_from_orders()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Most Visited Days Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(80, 10, txt="Date", align='L', fill=True)
        pdf.cell(80, 10, txt="Number of Orders", align='R', fill=True)
        pdf.ln(10)

        for index, (date, count) in enumerate(sorted(order_days.items(), key=lambda x: x[1], reverse=True), start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(80, 10, txt=date, align='L')
            pdf.cell(80, 10, txt=str(count), align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'most_visited_days_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")
