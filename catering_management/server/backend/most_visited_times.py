import json
import os
from fpdf import FPDF
from tkinter import messagebox
import time
from backend.save_data import SaveData
from datetime import datetime

class VisitedTimes:
    order_times_file = 'order_times.json'

    def __init__(self, order_times_file_path='order_times.json'):
        self.order_times_file_path = order_times_file_path
        self.order_times = self.load_order_times()

    @staticmethod
    def load_order_times():
        if os.path.exists(VisitedTimes.order_times_file):
            with open(VisitedTimes.order_times_file, 'r') as file:
                return json.load(file)
        return []

    @staticmethod
    def update_order_times():
        orders = SaveData.load_orders()
        order_times = []
        for order in orders:
            human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order["start_time"]))
            order_times.append({"transaction_id": order["transaction_id"], "start_time": human_readable_time})
        with open(VisitedTimes.order_times_file, 'w') as file:
            json.dump(order_times, file, indent=4)

    @staticmethod
    def extract_order_times_from_orders():
        orders = SaveData.load_orders()
        order_times = []
        for order in orders:
            human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order["start_time"]))
            order_times.append({"transaction_id": order["transaction_id"], "start_time": human_readable_time})
        with open(VisitedTimes.order_times_file, 'w') as file:
            json.dump(order_times, file, indent=4)

    def print_most_visited_times(self):
        VisitedTimes.extract_order_times_from_orders()
        order_times = VisitedTimes.load_order_times()
        time_counts = {}
        for entry in order_times:
            order_time = datetime.strptime(entry["start_time"], '%Y-%m-%d %H:%M:%S').strftime('%H:00')
            if order_time in time_counts:
                time_counts[order_time] += 1
            else:
                time_counts[order_time] = 1

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt="Most Visited Times Report", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(10, 10, txt="", align='L', fill=True)
        pdf.cell(80, 10, txt="Time", align='L', fill=True)
        pdf.cell(80, 10, txt="Number of Orders", align='R', fill=True)
        pdf.ln(10)

        for index, (time, count) in enumerate(sorted(time_counts.items(), key=lambda x: x[1], reverse=True), start=1):
            pdf.cell(10, 10, txt=str(index), align='L')
            pdf.cell(80, 10, txt=time, align='L')
            pdf.cell(80, 10, txt=str(count), align='R')
            pdf.ln(10)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'most_visited_times_report.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Report has been printed to {pdf_output_path}")
