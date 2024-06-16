import tkinter as tk
from tkinter import ttk, messagebox
import time
from fpdf import FPDF
import os
from tkcalendar import DateEntry
from backend.save_data import SaveData

class OrdersPage(tk.Frame):
    def __init__(self, master, server_page, orders):
        super().__init__(master, bg="#1F2836")
        self.server_page = server_page
        self.orders = orders
        self.filtered_orders = orders  # Initialize filtered_orders with all orders
        self.pack(fill=tk.BOTH, expand=True)
        self.create_order_frame()
        self.create_filter_buttons()
        self.display_orders()
        self.update_remaining_time()  # Start the countdown update

    def create_order_frame(self):
        self.order_frame = tk.Frame(self, bg="#1F2836")
        self.order_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.order_frame, bg="#1F2836")
        self.scrollbar = ttk.Scrollbar(self.order_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1F2836")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def create_filter_buttons(self):
        button_frame = tk.Frame(self, bg="#1F2836")
        button_frame.pack(fill=tk.X, pady=10)

        self.date_entry = DateEntry(button_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        show_all_orders_button = tk.Button(button_frame, text="Show All Orders", command=self.display_orders, bg="#2ECC71", fg="white")
        show_all_orders_button.pack(side=tk.LEFT, padx=5)

        show_orders_per_day_button = tk.Button(button_frame, text="Show Orders Per Day", command=self.display_orders_per_day, bg="#2ECC71", fg="white")
        show_orders_per_day_button.pack(side=tk.LEFT, padx=5)

        show_items_not_finished_button = tk.Button(button_frame, text="Show Items Ordered Not Finished", command=self.display_items_not_finished, bg="#2ECC71", fg="white")
        show_items_not_finished_button.pack(side=tk.LEFT, padx=5)

    def display_orders(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, order in enumerate(self.filtered_orders):
            order_frame = tk.Frame(self.scrollable_frame, bg="#1F2836", bd=2, relief=tk.RIDGE)
            order_frame.pack(fill=tk.X, pady=5, padx=5)

            order_text = f"Order {index + 1}:\n"
            order_text += f"Transaction ID: {order.get('transaction_id', '')}\n"
            order_text += f"First Name: {order.get('first_name', '')}\n"
            order_text += f"Last Name: {order.get('last_name', '')}\n"
            order_text += f"Phone Number: {order.get('phone_number', '')}\n"
            order_text += f"Address: {order.get('address', '')}\n"
            order_text += f"Details: {order.get('details', '')}\n"
            order_text += f"Customer Code: {order.get('customer_code', '')}\n"
            order_text += "Items:\n"

            items_count = order.get('order', {})
            for item, count in items_count.items():
                price = SaveData.get_item_price(item)
                order_text += f"{item}: {count} x {price}\n"
            order_text += f"Total Price: {order.get('total_price', '')}\n"
            order_text += f"Discount: {order.get('discount', '')}%\n"
            order_text += f"Final Price: {SaveData.apply_discount(order.get('total_price', 0), order.get('discount', 0))}\n"
            order_text += f"Preparation Time: {order.get('prep_time', '')} minutes\n"

            if 'start_time' in order:
                human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order['start_time']))
                order_text += f"Start Time: {human_readable_time}\n"
            if 'remaining_time' in order:
                remaining_time = order.get('remaining_time', '')
                order_text += f"Remaining Time: {remaining_time} minutes\n"
                if remaining_time == 0:
                    order_text += "Order is finished\n"

            label = tk.Label(order_frame, text=order_text, bg="#1F2836", fg="#F2F2F2", justify=tk.LEFT)
            label.pack(anchor="w", side=tk.LEFT)

            edit_button = tk.Button(order_frame, text="Edit Order", command=lambda o=order: self.edit_order(o), bg="#3498DB", fg="white")
            edit_button.pack(side=tk.RIGHT)

            print_button = tk.Button(order_frame, text="Print Order", command=lambda o=order: self.print_order(o), bg="#2ECC71", fg="white")
            print_button.pack(side=tk.RIGHT, padx=5)



    def display_items_not_finished(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        items = {}
        for order in self.orders:
            if order.get('remaining_time', 0) > 0:
                for item, count in order["order"].items():
                    if item in items:
                        items[item] += count
                    else:
                        items[item] = count

        for item, count in items.items():
            item_frame = tk.Frame(self.scrollable_frame, bg="#1F2836", bd=2, relief=tk.RIDGE)
            item_frame.pack(fill=tk.X, pady=5, padx=5)

            item_text = f"{item}: {count}"
            label = tk.Label(item_frame, text=item_text, bg="#1F2836", fg="#F2F2F2", font=("Arial", 14), justify=tk.LEFT)
            label.pack(anchor="w", side=tk.LEFT, padx=10, pady=5)

    def display_orders_per_day(self):
        selected_date = self.date_entry.get_date().strftime("%Y-%m-%d")
        self.filtered_orders = [order for order in self.orders if time.strftime("%Y-%m-%d", time.localtime(order['start_time'])) == selected_date]
        self.display_orders()

    def edit_order(self, order):
        self.server_page.show_menu_page(order_to_edit=order)


    def submit_order_details(self, first_name, last_name, phone_number, address, details, transaction_id, new_customer, customer_code, window, order_to_edit):
        order_dict = {}
        for item_name, item_data in self.item_frames.items():
            quantity = item_data["quantity"]
            if quantity > 0:
                order_dict[item_name] = quantity

        if new_customer or not customer_code:
            code_data = SaveData.get_or_generate_code(first_name, last_name)
            customer_code = code_data['code']
            discount = code_data['discount']
            usage = 0
        else:
            code_data = SaveData.increment_code_usage(customer_code) if not order_to_edit else None
            if code_data:
                discount = code_data['discount']
                usage = code_data['uses']
            else:
                discount = 0

        total_price = sum(SaveData.get_item_price(item) * count for item, count in order_dict.items())
        discounted_price = SaveData.apply_discount(total_price, discount)

        new_order = {
            "order": order_dict,
            "start_time": time.time(),
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "address": address,
            "details": details,
            "transaction_id": transaction_id,
            "customer_code": customer_code,
            "prep_time": max(SaveData.get_item_prep_time(item) for item in order_dict),
            "total_price": discounted_price,
            "discount": discount
        }

        if order_to_edit:
            original_order = next(order for order in self.orders if order["transaction_id"] == transaction_id)
            for i, order in enumerate(self.orders):
                if order["transaction_id"] == transaction_id:
                    self.orders[i] = new_order
                    break
            SaveData.save_orders(self.orders)
            correction = {
                "transaction_id": transaction_id,
                "customer_name": f"{first_name} {last_name}",
                "original_order_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(original_order["start_time"])),
                "modification_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                "changes_made": self.get_changes_made(original_order, new_order)
            }
            print(f"Saving correction: {correction}")  # Debug statement
            SaveData.save_order_correction(correction)
        else:
            self.orders.append(new_order)
            SaveData.save_orders(self.orders)
            SaveData.save_order_time(transaction_id, new_order["start_time"])

        window.destroy()
        self.server_page.show_orders_page()




    def print_order(self, order):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(200, 10, txt=f"Transaction ID: {order['transaction_id']}", ln=True, fill=True)
        pdf.set_font("Arial", size=12)

        pdf.cell(50, 10, txt=f"First Name: {order.get('first_name', '')}", ln=0)
        pdf.cell(100, 10, txt=f"Last Name: {order.get('last_name', '')}", ln=True, align='C')

        pdf.cell(50, 10, txt=f"Phone Number: {order.get('phone_number', '')}", ln=0)
        pdf.cell(100, 10, txt=f"Address: {order.get('address', '')}", ln=True, align='C')

        pdf.cell(200, 10, txt=f"Details: {order.get('details', '')}", ln=True)
        pdf.cell(200, 10, txt=f"Customer Code: {order.get('customer_code', '')}", ln=True)

        pdf.cell(200, 10, txt="Order:", ln=True, fill=True)
        pdf.cell(80, 10, txt="Item", border=1)
        pdf.cell(40, 10, txt="Quantity", border=1)
        pdf.cell(40, 10, txt="Price", border=1)
        pdf.cell(30, 10, txt="Total Price:", border=1)
        pdf.ln()

        total_price = 0
        for item, count in order["order"].items():
            price = SaveData.get_item_price(item)
            item_total_price = price * count
            pdf.cell(80, 10, txt=item, border=1)
            pdf.cell(40, 10, txt=str(count), border=1)
            pdf.cell(40, 10, txt=str(price), border=1)
            pdf.cell(30, 10, txt=str(item_total_price), border=1)
            pdf.ln()
            total_price += item_total_price

        pdf.cell(200, 10, txt=f"Total Price: {total_price}", ln=True)
        pdf.cell(200, 10, txt=f"Discount: {order.get('discount', '')}%", ln=True)
        final_price = SaveData.apply_discount(total_price, order.get('discount', 0))
        pdf.cell(200, 10, txt=f"Final Price: {final_price}", ln=True)

        pdf.cell(200, 10, txt=f"Preparation Time: {order.get('prep_time', '')} minutes", ln=True)
        human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order.get('start_time', 0)))
        pdf.cell(200, 10, txt=f"Start Time: {human_readable_time}", ln=True)

        pdf_output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'receipts', f"order_{order['transaction_id']}.pdf")
        pdf.output(pdf_output_path)
        messagebox.showinfo("Success", f"Order has been printed to {pdf_output_path}")

    def update_remaining_time(self):
        current_time = time.time()
        for order in self.orders:
            if 'prep_time' in order and 'start_time' in order:
                elapsed_time = (current_time - order['start_time']) / 60  # Convert to minutes
                remaining_time = max(order['prep_time'] - elapsed_time, 0)
                order['remaining_time'] = int(remaining_time)

        self.orders.sort(key=lambda x: (x['remaining_time'] != 0, x['remaining_time']))  # Sort orders
        self.display_orders()
        self.after(60000, self.update_remaining_time)  # Update every minute