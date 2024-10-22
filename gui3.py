# Detailed GUI for the OBD 2 Reader

import tkinter as tk
from tkinter import ttk
import obd
import threading

class OBDApp:
    def __init__(self, master):
        self.master = master
        master.title("OBD-II Dashboard")
        master.geometry("800x800")  # Set the window size

        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Poppins", 14), padding=10)
        style.configure("TButton", font=("Poppins", 12), padding=5)

        # Create a frame for dashboard
        self.dashboard_frame = ttk.Frame(master)
        self.dashboard_frame.pack(pady=20)

        # Create labels for different OBD-II parameters
        self.speed_label = ttk.Label(self.dashboard_frame, text="Speed: N/A")
        self.speed_label.grid(row=0, column=0, padx=10, pady=10)

        self.rpm_label = ttk.Label(self.dashboard_frame, text="RPM: N/A")
        self.rpm_label.grid(row=1, column=0, padx=10, pady=10)

        self.fuel_level_label = ttk.Label(self.dashboard_frame, text="Fuel Level: N/A")
        self.fuel_level_label.grid(row=2, column=0, padx=10, pady=10)

        self.coolant_temp_label = ttk.Label(self.dashboard_frame, text="Coolant Temp: N/A")
        self.coolant_temp_label.grid(row=0, column=1, padx=10, pady=10)

        self.engine_load_label = ttk.Label(self.dashboard_frame, text="Engine Load: N/A")
        self.engine_load_label.grid(row=1, column=1, padx=10, pady=10)

        self.throttle_pos_label = ttk.Label(self.dashboard_frame, text="Throttle Position: N/A")
        self.throttle_pos_label.grid(row=2, column=1, padx=10, pady=10)

        self.intake_temp_label = ttk.Label(self.dashboard_frame, text="Intake Temp: N/A")
        self.intake_temp_label.grid(row=0, column=2, padx=10, pady=10)

        self.vehicle_speed_label = ttk.Label(self.dashboard_frame, text="Vehicle Speed: N/A")
        self.vehicle_speed_label.grid(row=1, column=2, padx=10, pady=10)

        self.mileage_label = ttk.Label(self.dashboard_frame, text="Mileage: N/A")
        self.mileage_label.grid(row=2, column=2, padx=10, pady=10)

        # Start and Stop Buttons
        self.start_button = ttk.Button(master, text="Start", command=self.start_reading)
        self.start_button.pack(pady=20)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_reading, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.connection = None
        self.running = False

    def start_reading(self):
        self.connection = obd.OBD()
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.read_data()

    def stop_reading(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def read_data(self):
        if self.running:
            # Define commands to query
            commands = {
                "speed": obd.commands.SPEED,
                "rpm": obd.commands.RPM,
                "fuel_level": obd.commands.FUEL_LEVEL,
                "coolant_temp": obd.commands.COOLANT_TEMP,
                "engine_load": obd.commands.ENGINE_LOAD,
                "throttle_pos": obd.commands.THROTTLE_POS,
                "intake_temp": obd.commands.INTAKE_TEMP,
                "vehicle_speed": obd.commands.SPEED,
                "mileage": obd.commands.DISTANCE_SINCE_DTC_CLEAR,
                "engine_runtime": obd.commands.RUN_TIME
            }

            # Get responses
            responses = {cmd: self.connection.query(command) for cmd, command in commands.items()}

            # Update labels with values
            self.speed_label.config(text=f"Speed: {responses['speed'].value.mph if responses['speed'].value else 'N/A'} mph")
            self.rpm_label.config(text=f"RPM: {responses['rpm'].value.rpm if responses['rpm'].value else 'N/A'} RPM")
            self.fuel_level_label.config(text=f"Fuel Level: {responses['fuel_level'].value.percent if responses['fuel_level'].value else 'N/A'}%")
            self.coolant_temp_label.config(text=f"Coolant Temp: {responses['coolant_temp'].value.celsius if responses['coolant_temp'].value else 'N/A'}°C")
            self.engine_load_label.config(text=f"Engine Load: {responses['engine_load'].value.percent if responses['engine_load'].value else 'N/A'}%")
            self.throttle_pos_label.config(text=f"Throttle Position: {responses['throttle_pos'].value.percent if responses['throttle_pos'].value else 'N/A'}%")
            self.intake_temp_label.config(text=f"Intake Temp: {responses['intake_temp'].value.celsius if responses['intake_temp'].value else 'N/A'}°C")
            self.vehicle_speed_label.config(text=f"Vehicle Speed: {responses['vehicle_speed'].value.mph if responses['vehicle_speed'].value else 'N/A'} mph")
            self.mileage_label.config(text=f"Mileage: {responses['mileage'].value.miles if responses['mileage'].value else 'N/A'} miles")

            self.master.after(1000, self.read_data)  # read every second

if __name__ == "__main__":
    root = tk.Tk()
    app = OBDApp(root)
    root.mainloop()