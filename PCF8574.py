import smbus
import time

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

    def set_pin(self, pin, value):
        """Set a single pin to high or low."""
        current_value = self.read()
        if value:
            current_value |= (1 << pin)
        else:
            current_value &= ~(1 << pin)
        self.write(current_value)

    def get_pin(self, pin):
        """Get the status of a single pin."""
        value = self.read()
        return (value >> pin) & 1

# Example usage
if __name__ == "__main__":
    expander = PCF8574(0x27)  # Replace 0x20 with your PCF8574's I2C address
    expander.set_pin(0, 1)  # Set P0 high
    print("Reading P0:", expander.get_pin(0))  # Read back P0
    expander.set_pin(0, 0)  # Set P0 low
