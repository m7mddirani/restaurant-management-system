import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from backend.save_data import SaveData
import time

class MenuPage(tk.Frame):
    def __init__(self, master, server_page, orders, order_to_edit=None, on_save=None):
        super().__init__(master)
        self.master = master
        self.server_page = server_page
        self.orders = orders
        self.order_to_edit = order_to_edit
        self.on_save = on_save
        self.configure(bg="#1F2836")

        self.item_frames = {}

        print("MenuPage: Initialized")

        self.canvas = tk.Canvas(self, bg="#1F2836")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
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

        self.create_groups(self.scrollable_frame)

    def create_groups(self, parent):
        groups = SaveData.get_menu_groups()
        row = 0

        for group_name, items in groups.items():
            tk.Label(parent, text=group_name, font=("Arial", 18), bg="#1F2836", fg="#F2F2F2").grid(row=row, column=0, columnspan=4, pady=10)
            row += 1

            for index, item in enumerate(items):
                col = index % 4
                self.create_item_frame(parent, item, row, col)
                if col == 3:
                    row += 1
            if col != 3:
                row += 1

        tk.Button(parent, text="Finish Order", command=self.finish_order, bg="#2ECC71", fg="white", font=("Arial", 14)).grid(row=row, column=1, pady=20)

    def create_item_frame(self, parent, item, row, col):
        frame = tk.Frame(parent, bg="#1F2836", bd=2)
        frame.grid(row=row, column=col, padx=5, pady=5)

        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "images", item["image"])
        image = Image.open(image_path)
        image = image.resize((80, 80), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(frame, image=photo)
        label.image = photo
        label.pack()

        label = tk.Label(frame, text=item["name"], bg="#1F2836", fg="#F2F2F2")
        label.pack()

        label = tk.Label(frame, text=f"Price: {item['price']}", bg="#1F2836", fg="#F2F2F2")
        label.pack()

        quantity_frame = tk.Frame(frame, bg="#1F2836")
        quantity_frame.pack()

        self.item_frames[item["name"]] = {"frame": frame, "quantity": 0, "price": item["price"], "prep_time": item["prep_time"]}

        increment_button = tk.Button(quantity_frame, text="+", command=lambda: self.increment(item["name"]))
        increment_button.grid(row=0, column=0)

        quantity_label = tk.Label(quantity_frame, text="0", bg="#1F2836", fg="#F2F2F2")
        quantity_label.grid(row=0, column=1)

        decrement_button = tk.Button(quantity_frame, text="-", command=lambda: self.decrement(item["name"]))
        decrement_button.grid(row=0, column=2)

        self.item_frames[item["name"]]["label"] = quantity_label

        if self.order_to_edit and item["name"] in self.order_to_edit["order"]:
            quantity = self.order_to_edit["order"][item["name"]]
            self.item_frames[item["name"]]["quantity"] = quantity
            quantity_label.config(text=str(quantity))

    def increment(self, item_name):
        self.item_frames[item_name]["quantity"] += 1
        self.item_frames[item_name]["label"].config(text=str(self.item_frames[item_name]["quantity"]))
        SaveData.add_item(item_name)

    def decrement(self, item_name):
        if self.item_frames[item_name]["quantity"] > 0:
            self.item_frames[item_name]["quantity"] -= 1
            self.item_frames[item_name]["label"].config(text=str(self.item_frames[item_name]["quantity"]))
            if item_name in SaveData._order:
                SaveData._order.remove(item_name)


    def finish_order(self):
        print("Finish Order button clicked")
        self.show_order_details_window()

    def show_order_details_window(self):
        window = tk.Toplevel(self)
        window.title("Order Details")
        window.geometry("400x400")
        window.configure(bg="#1F2836")

        tk.Label(window, text="First Name", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        first_name_entry = tk.Entry(window)
        first_name_entry.pack(pady=5)

        tk.Label(window, text="Last Name", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        last_name_entry = tk.Entry(window)
        last_name_entry.pack(pady=5)

        tk.Label(window, text="Phone Number", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        phone_number_entry = tk.Entry(window)
        phone_number_entry.pack(pady=5)

        tk.Label(window, text="Address", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        address_entry = tk.Entry(window)
        address_entry.pack(pady=5)

        tk.Label(window, text="Details", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        details_entry = tk.Entry(window)
        details_entry.pack(pady=5)

        tk.Label(window, text="Transaction ID", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        transaction_id_entry = tk.Entry(window)
        transaction_id_entry.pack(pady=5)

        new_customer_var = tk.BooleanVar()
        tk.Checkbutton(window, text="New Customer", variable=new_customer_var, bg="#1F2836", fg="#F2F2F2").pack(pady=5)

        tk.Label(window, text="Customer Code (if any)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        customer_code_entry = tk.Entry(window)
        customer_code_entry.pack(pady=5)

        if self.order_to_edit:
            first_name_entry.insert(0, self.order_to_edit.get('first_name', ''))
            last_name_entry.insert(0, self.order_to_edit.get('last_name', ''))
            phone_number_entry.insert(0, self.order_to_edit.get('phone_number', ''))
            address_entry.insert(0, self.order_to_edit.get('address', ''))
            details_entry.insert(0, self.order_to_edit.get('details', ''))
            transaction_id_entry.insert(0, self.order_to_edit.get('transaction_id', ''))
            customer_code_entry.insert(0, self.order_to_edit.get('customer_code', ''))

        submit_button = tk.Button(window, text="Submit", command=lambda: self.submit_order_details(
            first_name_entry.get(),
            last_name_entry.get(),
            phone_number_entry.get(),
            address_entry.get(),
            details_entry.get(),
            transaction_id_entry.get(),
            new_customer_var.get(),
            customer_code_entry.get(),
            window
        ), bg="#2ECC71", fg="white")
        submit_button.pack(pady=10)

    def submit_order_details(self, first_name, last_name, phone_number, address, details, transaction_id, new_customer, customer_code, window):
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
            code_data = SaveData.increment_code_usage(customer_code) if not self.order_to_edit else None
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

        if self.order_to_edit:
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

    def get_changes_made(self, original_order, new_order):
        changes = []
        for item, qty in new_order["order"].items():
            if item not in original_order["order"]:
                changes.append(f"Added {item} (x{qty})")
            elif original_order["order"][item] != qty:
                changes.append(f"Changed quantity of {item} from {original_order['order'][item]} to {qty}")
        for item in original_order["order"]:
            if item not in new_order["order"]:
                changes.append(f"Removed {item}")
        return ", ".join(changes)
