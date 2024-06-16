import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class WarehousePage(tk.Frame):
    def __init__(self, master, warehouse):
        super().__init__(master)
        self.warehouse = warehouse
        self.pack(fill=tk.BOTH, expand=True)
        self.create_warehouse_frame()

    def create_warehouse_frame(self):
        script_dir = os.path.dirname(__file__)
        bg_image_path = os.path.join(script_dir, "images", "persia-nov19issue-may20-saghar.jpg")

        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        warehouse_frame = tk.Frame(self.bg_label)  # Removed background color
        warehouse_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(warehouse_frame, bg="#1F2836")
        self.scrollbar = ttk.Scrollbar(warehouse_frame, orient="vertical", command=self.canvas.yview)
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

        self.display_warehouse()

    def display_warehouse(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Warehouse", font=("Arial", 18), bg="#1F2836", fg="#F2F2F2").pack(pady=10)

        add_button = tk.Button(self.scrollable_frame, text="Add Material", command=self.add_material_window, bg="grey", fg="white")
        add_button.pack(pady=10)

        materials = self.warehouse.get_materials()
        for material in materials:
            material_frame = tk.Frame(self.scrollable_frame, bg="#1F2836")
            material_frame.pack(fill=tk.X, pady=5)

            material_text = (
                f"Name: {material['name']}\n"
                f"Price: {material['price']}\n"
                f"Entry Date: {material['entry_date']}\n"
                f"Production Date: {material['production_date']}\n"
                f"Expiration Date: {material['expiration_date']}\n"
                f"Quantity: {material['quantity']} {material['unit']}"
            )
            tk.Label(material_frame, text=material_text, bg="#1F2836", fg="#F2F2F2", justify=tk.LEFT).pack(anchor="w", side=tk.LEFT)

            remove_button = tk.Button(material_frame, text="Remove", command=lambda m=material: self.remove_material(m['name']), bg="grey", fg="white")
            remove_button.pack(side=tk.RIGHT, padx=5)

            edit_button = tk.Button(material_frame, text="Edit", command=lambda m=material: self.edit_material_window(m), bg="grey", fg="white")
            edit_button.pack(side=tk.RIGHT)

    def add_material_window(self):
        window = tk.Toplevel(self)
        window.title("Add Material")
        window.geometry("300x450")
        window.configure(bg="#1F2836")

        tk.Label(window, text="Name", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        name_entry = tk.Entry(window)
        name_entry.pack(pady=5)

        tk.Label(window, text="Price", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        price_entry = tk.Entry(window)
        price_entry.pack(pady=5)

        tk.Label(window, text="Entry Date (YYYY-MM-DD)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        entry_date_entry = tk.Entry(window)
        entry_date_entry.pack(pady=5)

        tk.Label(window, text="Production Date (YYYY-MM-DD)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        production_date_entry = tk.Entry(window)
        production_date_entry.pack(pady=5)

        tk.Label(window, text="Expiration Date (YYYY-MM-DD)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        expiration_date_entry = tk.Entry(window)
        expiration_date_entry.pack(pady=5)

        tk.Label(window, text="Quantity", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        quantity_entry = tk.Entry(window)
        quantity_entry.pack(pady=5)

        tk.Label(window, text="Unit", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        unit_entry = tk.Entry(window)
        unit_entry.pack(pady=5)

        submit_button = tk.Button(window, text="Submit", command=lambda: self.add_material(
            name_entry.get(),
            price_entry.get(),
            entry_date_entry.get(),
            production_date_entry.get(),
            expiration_date_entry.get(),
            quantity_entry.get(),
            unit_entry.get(),
            window
        ), bg="grey", fg="white")
        submit_button.pack(pady=10)

    def add_material(self, name, price, entry_date, production_date, expiration_date, quantity, unit, window):
        self.warehouse.add_material(name, price, entry_date, production_date, expiration_date, quantity, unit)
        window.destroy()
        self.display_warehouse()

    def remove_material(self, name):
        self.warehouse.remove_material(name)
        self.display_warehouse()

    def edit_material_window(self, material):
        window = tk.Toplevel(self)
        window.title("Edit Material")
        window.geometry("300x400")
        window.configure(bg="#1F2836")

        tk.Label(window, text="Name", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        name_entry = tk.Entry(window)
        name_entry.insert(0, material['name'])
        name_entry.pack(pady=5)

        tk.Label(window, text="Price", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        price_entry = tk.Entry(window)
        price_entry.insert(0, material['price'])
        price_entry.pack(pady=5)

        tk.Label(window, text="Entry Date (YYYY-MM-DD)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        entry_date_entry = tk.Entry(window)
        entry_date_entry.insert(0, material['entry_date'])
        entry_date_entry.pack(pady=5)

        tk.Label(window, text="Production Date (YYYY-MM-DD)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        production_date_entry = tk.Entry(window)
        production_date_entry.insert(0, material['production_date'])
        production_date_entry.pack(pady=5)

        tk.Label(window, text="Expiration Date (YYYY-MM-DD)", bg="#1F2836", fg="#F2F2F2").pack(pady=5)
        expiration_date_entry = tk.Entry(window)
        expiration_date_entry.insert(0, material['expiration_date'])
        expiration_date_entry.pack(pady=5)

        submit_button = tk.Button(window, text="Submit", command=lambda: self.update_material(
            material['name'],
            {
                'name': name_entry.get(),
                'price': price_entry.get(),
                'entry_date': entry_date_entry.get(),
                'production_date': production_date_entry.get(),
                'expiration_date': expiration_date_entry.get()
            },
            window
        ), bg="grey", fg="white")
        submit_button.pack(pady=10)

    def update_material(self, original_name, updated_info, window):
        self.warehouse.update_material(original_name, updated_info)
        window.destroy()
        self.display_warehouse()
