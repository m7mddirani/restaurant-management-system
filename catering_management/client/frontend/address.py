import os
import time
import tkinter as tk
from tkinter import messagebox

from backend.send_data import SendData
from backend.save_data import SaveData

class AddressPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#dbd7cd")
        self.master.geometry("500x300")
        print("AddressPage: Initialized")


        
        self.frame = tk.Frame(self, bg="#dbd7cd", bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame, text="First Name", bg="#dbd7cd", fg="#334e41").grid(row=0, column=0, padx=5, pady=5)
        self.first_name = tk.Entry(self.frame, bg="#dbd7cd", fg="#334e41")
        self.first_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.frame, text="Last Name", bg="#dbd7cd", fg="#334e41").grid(row=1, column=0, padx=5, pady=5)
        self.last_name = tk.Entry(self.frame, bg="#dbd7cd", fg="#334e41")
        self.last_name.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.frame, text="Phone Number", bg="#dbd7cd", fg="#334e41").grid(row=2, column=0, padx=5, pady=5)
        self.phone_number = tk.Entry(self.frame, bg="#dbd7cd", fg="#334e41")
        self.phone_number.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.frame, text="Address", bg="#dbd7cd", fg="#334e41").grid(row=3, column=0, padx=5, pady=5)
        self.address = tk.Entry(self.frame, bg="#dbd7cd", fg="#334e41")
        self.address.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self.frame, text="Details", bg="#dbd7cd", fg="#334e41").grid(row=4, column=0, padx=5, pady=5)
        self.details = tk.Entry(self.frame, bg="#dbd7cd", fg="#334e41")
        self.details.grid(row=4, column=1, padx=5, pady=5)

        new_customer_var = tk.BooleanVar()
        tk.Checkbutton(self.frame, text="New Customer", variable=new_customer_var, bg="#dbd7cd", fg="#334e41").grid(row=5, column=0, padx=5, pady=5)

        tk.Label(self.frame, text="Customer Code (if any)", bg="#dbd7cd", fg="#334e41").grid(row=5, column=1, padx=5, pady=5)
        self.customer_code = tk.Entry(self.frame, bg="#dbd7cd", fg="#334e41")
        self.customer_code.grid(row=5, column=2, padx=5, pady=5)
        
        submit_button = tk.Button(self.frame, text="Submit", command=lambda: self.submit_order(new_customer_var.get()), bg="#334e41", fg="#dbd7cd")
        submit_button.grid(row=6, columnspan=2, pady=10)
        
        print("AddressPage: Components added")

    def submit_order(self, new_customer):
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        phone_number = self.phone_number.get()
        address = self.address.get()
        details = self.details.get()
        customer_code = self.customer_code.get()

        order = SaveData.get_order()
        if order is None:
            messagebox.showerror("Error", "Order data is missing.")
            return

        # Convert order to dictionary format
        order_dict = {}
        for item in order:
            if item in order_dict:
                order_dict[item] += 1
            else:
                order_dict[item] = 1

        save_data = SaveData()
        if new_customer or not customer_code:
            code_data = save_data.get_or_generate_code(first_name, last_name)
            customer_code = code_data['code']
            discount = code_data['discount']
            usage = 0
        else:
            code_data = save_data.increment_code_usage(customer_code)
            if code_data:
                discount = code_data['discount']
                usage = code_data['uses']
            else:
                messagebox.showerror("Error", "Invalid customer code")
                return

        total_price = sum(SaveData.get_item_price(item) * count for item, count in order_dict.items())
        discounted_price = SaveData.apply_discount(total_price, discount)

        transaction_id = self.generate_transaction_id()

        order_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "address": address,
            "details": details,
            "transaction_id": transaction_id,
            "order": order_dict,
            "customer_code": customer_code,
            "total_price": discounted_price,
            "discount": discount,
            "start_time": time.time()
        }

        response = SendData.send_order(order_data)
        
        if response and response.get("status") == "received":
            SaveData.reset_order()  # Reset the order after successful submission
            from frontend.menu import MenuPage
            self.master.switch_frame(MenuPage)
            messagebox.showinfo("Success", "Order submitted successfully.")
        else:
            messagebox.showerror("Error", "Failed to submit order. Please try again.")

    def generate_transaction_id(self):
        current_date = time.strftime("%Y-%m-%d")
        transaction_count = SaveData.get_transaction_count(current_date)
        SaveData.increment_transaction_count()
        return f"{transaction_count:03d}"
