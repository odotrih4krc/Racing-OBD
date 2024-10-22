# Gui used with the data.py file

import tkinter as tk
from tkinter import ttk
import obd
import threading
import time

class OBDReader:
    def __init__(self):
        self.connection = obd.OBD()  # Automatically detect the OBD-II interface

    def get_values(self):
        values = {
            "speed": self.get_speed(),
            "rpm": self.get_rpm(),
            "fuel_level": self.get_fuel_level(),
            "coolant_temp": self.get_coolant_temp()
        }
        return values

    def get_speed(self):
        response = self.connection.query(obd.commands.SPEED)
        return response.value.mph if response.value else "N/A"

    def get_rpm(self):
        response = self.connection.query(obd.commands.RPM)
        return response.value.rpm if response.value else "N/A"

    def get_fuel_level(self):
        response = self.connection.query(obd.commands.FUEL_LEVEL)
        return response.value.percent if response.value else "N/A"

    def get_coolant_temp(self):
        response = self.connection.query(obd.commands.COOLANT_TEMP)
        return response.value.celsius if response.value else "N/A"

class OBDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OHMYPY OBD ODOT")
        self.root.geometry("600x550")

        # Create the OBDReader instance
        self.obd_reader = OBDReader()

        # Create UI elements (cards)
        self.create_card("Speed: N/A", "Speed (mph)", 0)
        self.create_card("RPM: N/A", "RPM", 1)
        self.create_card("Fuel Level: N/A", "Fuel Level (%)", 2)
        self.create_card("Oil Level: N/A", "Oil Level (%)", 3)
        self.create_card("Coolant Temp: N/A", "Coolant Temp (°C)", 4)
        

        # Start/Stop Buttons
        self.start_button = ttk.Button(root, text="Start Reading", command=self.start_reading)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Reading", command=self.stop_reading, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.running = False

    def create_card(self, initial_text, title, row):
        card = ttk.Frame(self.root, padding=10, relief="groove")
        card.pack(pady=5, fill=tk.X)

        title_label = ttk.Label(card, text=title, font=("Poppins", 14))
        title_label.pack()

        value_label = ttk.Label(card, text=initial_text, font=("Poppins", 18))
        value_label.pack()

        # Store the value label in an attribute to update later
        setattr(self, f"value_label_{row}", value_label)

    def start_reading(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.read_values, daemon=True).start()

    def stop_reading(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def read_values(self):
        while self.running:
            values = self.obd_reader.get_values()
            # Update the labels with the new values
            self.update_value_label(0, f"Speed: {values['speed']} mph")
            self.update_value_label(1, f"RPM: {values['rpm']}")
            self.update_value_label(2, f"Fuel Level: {values['fuel_level']}%")
            self.update_value_label(3, f"Oil Level: {values['oil_level']} %")
            self.update_value_label(3, f"Coolant Temp: {values['coolant_temp']} °C")
            

            time.sleep(1)  # Update every second

    def update_value_label(self, index, text):
        label = getattr(self, f"value_label_{index}")
        label.config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = OBDApp(root)
    root.mainloop()