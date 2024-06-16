import json
import os
from fpdf import FPDF
from tkinter import messagebox
import time

class CustomerHistory:
    orders_file = 'orders.json'

    def __init__(self, orders_file_path='orders.json'):
        self.orders_file_path = orders_file_path
        self.orders = self.load_orders()

    @staticmethod
    def load_orders():
        if os.path.exists(CustomerHistory.orders_file):
            with open(CustomerHistory.orders_file, 'r') as file:
                return json.load(file)
        return []

    def get_customer_history(self, customer_name):
        customer_orders = []
        for order in self.orders:
            if isinstance(order, dict):
                if f"{order.get('first_name', '')} {order.get('last_name', '')}" == customer_name:
                    customer_orders.append(order)
        return customer_orders

    def print_customer_history(self, customer_name):
        customer_orders = self.get_customer_history(customer_name)

        if not customer_orders:
            messagebox.showinfo("No Orders", f"No orders found for customer {customer_name}")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(0, 10, txt=f"Customer Order History: {customer_name}", ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(40, 10, txt="Transaction ID", border=1)
        pdf.cell(40, 10, txt="Order Date", border=1)
        pdf.cell(70, 10, txt="Items Ordered", border=1)
        pdf.cell(40, 10, txt="Total Amount", border=1)
        pdf.ln()

        for order in customer_orders:
            transaction_id = order['transaction_id']
            order_date = time.strftime("%Y-%m-%d", time.localtime(order['start_time']))
            items_ordered = ', '.join(order['order'].keys())
            total_amount = order['total_price']

            pdf.cell(40, 10, txt=str(transaction_id), border=1)
            pdf.cell(40, 10, txt=order_date, border=1)
            pdf.cell(70, 10, txt=items_ordered, border=1)
            pdf.cell(40, 10, txt=f"{total_amount}", border=1)
            pdf.ln()

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', f'{customer_name}_order_history.pdf')
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Customer order history has been printed to {pdf_output_path}")
