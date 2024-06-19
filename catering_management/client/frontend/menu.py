import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from backend.save_data import SaveData

class MenuPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#dbd7cd")
        self.master.geometry("800x703") 
        self.item_frames = {}  # Initialize item_frames here

        print("MenuPage: Initialized")  # Debugging statement

        canvas = tk.Canvas(self, bg="#dbd7cd")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#dbd7cd")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="center")  # Anchor to the center
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_groups(scrollable_frame)

    def create_groups(self, parent):
        groups = SaveData.get_menu_groups()
        row = 0

        for group_name, items in groups.items():
            tk.Label(parent, text=group_name, font=("Arial", 18), bg="#dbd7cd", fg="#324e41").grid(row=row, column=0, columnspan=4, pady=10)
            row += 1

            for index, item in enumerate(items):
                col = index % 4
                self.create_item_frame(parent, item, row, col)
                if col == 3:
                    row += 1
            if col != 3:
                row += 1

        tk.Button(parent, text="Finish Order", command=self.finish_order, bg="#334e41", fg="white", font=("Arial", 14)).grid(row=row, column=1, pady=20)

    def create_item_frame(self, parent, item, row, col):
        frame = tk.Frame(parent, bg="#dbd7cd", bd=2)
        frame.grid(row=row, column=col, padx=5, pady=5)

        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "images", item["image"])
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.LANCZOS)  # Resize the images to be smaller
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(frame, image=photo)
        label.image = photo
        label.pack()

        label = tk.Label(frame, text=item["name"], bg="#dbd7cd", fg="#324e41")
        label.pack()

        label = tk.Label(frame, text=f"Price: {item['price']}", bg="#dbd7cd", fg="#324e41")
        label.pack()

        quantity_frame = tk.Frame(frame, bg="#dbd7cd")
        quantity_frame.pack()

        self.item_frames[item["name"]] = {"frame": frame, "quantity": 0}

        increment_button = tk.Button(quantity_frame,bg="#334e41", fg="white", text="+", command=lambda: self.increment(item["name"]))
        increment_button.grid(row=0, column=0)

        quantity_label = tk.Label(quantity_frame, text="0", bg="#dbd7cd", fg="#324e41")
        quantity_label.grid(row=0, column=1)

        decrement_button = tk.Button(quantity_frame,bg="#334e41", fg="white", text="-", command=lambda: self.decrement(item["name"]))
        decrement_button.grid(row=0, column=2)

        self.item_frames[item["name"]]["label"] = quantity_label

    def increment(self, item_name):
        self.item_frames[item_name]["quantity"] += 1
        self.item_frames[item_name]["label"].config(text=str(self.item_frames[item_name]["quantity"]))
        SaveData.add_item(item_name)

    def decrement(self, item_name):
        if self.item_frames[item_name]["quantity"] > 0:
            self.item_frames[item_name]["quantity"] -= 1
            self.item_frames[item_name]["label"].config(text=str(self.item_frames[item_name]["quantity"]))
            SaveData._order.remove(item_name)

    def finish_order(self):
        print("Finish Order button clicked")  # Debugging statement
        from frontend.address import AddressPage  # Deferred import to avoid circular import issue
        self.master.switch_frame(AddressPage)
