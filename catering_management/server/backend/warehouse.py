import os 
import json

class Warehouse:
    def __init__(self, file_path='warehouse_data.json'):
        self.file_path = file_path
        self.materials = self.load_materials()

    def load_materials(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def save_materials(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.materials, file, indent=4)

    def add_material(self, name, price, entry_date, production_date, expiration_date, quantity, unit):
        self.materials.append({
            'name': name,
            'price': price,
            'entry_date': entry_date,
            'production_date': production_date,
            'expiration_date': expiration_date,
            'quantity': quantity,
            'unit': unit
        })
        self.save_materials()

    def remove_material(self, name):
        self.materials = [m for m in self.materials if m['name'] != name]
        self.save_materials()

    def update_material(self, original_name, updated_info):
        for material in self.materials:
            if material['name'] == original_name:
                material.update(updated_info)
                break
        self.save_materials()

    def get_materials(self):
        return self.materials
