import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
import json
from datetime import datetime
from backend.save_data import SaveData
from tkcalendar import DateEntry

class CustomerReport:

    customer_codes_file = 'customer_codes.json'

    def __init__(self, customer_codes_file_path='customer_codes.json'):
        self.customer_codes_file = customer_codes_file_path
        self.customer_codes = self.load_customer_codes()

    @staticmethod
    def load_customer_codes():
        if os.path.exists(CustomerReport.customer_codes_file):
            with open(SaveData.customer_codes_file, 'r') as file:
                return json.load(file)
        return {}

    @staticmethod
    def get_valuable_customers():
        codes = CustomerReport.load_customer_codes()
        sorted_codes = sorted(codes.items(), key=lambda x: x[1]["uses"], reverse=True)
        return [{"code": code, "first_name": data["first_name"], "last_name": data["last_name"], "uses": data["uses"]} for code, data in sorted_codes if data["uses"] > 0]

    def create_reports_frame(self):
        self.reports_frame = tk.Frame(self, bg="#1F2836")
        self.reports_frame.pack(fill=tk.BOTH, expand=True)

        self.date_entry = DateEntry(self.reports_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=10)

        self.print_customers_button = tk.Button(self.reports_frame, text="Print Valuable Customers", command=self.print_customers, bg="#2ECC71", fg="white")
        self.print_customers_button.pack(pady=10)

    def print_customers(self):
        customers = CustomerReport.load_customer_codes()
        sorted_customers = sorted(customers.items(), key=lambda x: x[1]["uses"], reverse=True)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Valuable Customers Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(60, 10, txt="Name", align='L', fill=True)
        pdf.cell(60, 10, txt="Customer Code", align='C', fill=True)
        pdf.cell(60, 10, txt="Visits", align='R', fill=True)
        pdf.ln(10)

        for index, (code, data) in enumerate(sorted_customers, start=1):
            name = f"{data['first_name']} {data['last_name']}"
            visits = data['uses']
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(60, 10, txt=name, align='L')
            pdf.cell(60, 10, txt=code, align='C')
            pdf.cell(60, 10, txt=str(visits), align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..','..','reports', 'valuable_customers_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")