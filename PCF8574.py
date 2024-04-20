import smbus

class PCF8574:
    def __init__(self, address, bus_number=1):
        self.address = address
        self.bus = smbus.SMBus(bus_number)

    def write(self, data):
        """Write an 8-bit data to the PCF8574."""
        self.bus.write_byte(self.address, data)

    def read(self):
        """Read an 8-bit data from the PCF8574."""
        return self.bus.read_byte(self.address)

    def write_pattern(self, pattern):
        """Write a binary pattern to the PCF8574."""
        # Convert binary string to integer
        data = int(pattern, 2)
        self.write(data)

    def get_pin(self, pin):
        """Get the status of a single pin."""
        value = self.read()
        return (value >> pin) & 1
    