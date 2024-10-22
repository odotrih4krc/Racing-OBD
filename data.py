import obd

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
    
    def get_oil_level(self):
        response = self.connection.query(obd.commands.OIL_LEVEL)
        return response.value.celsius if response.value else "N/A"