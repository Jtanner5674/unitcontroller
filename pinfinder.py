import smbus
import time

class PCF8574:
    def __init__(self, address, bus_number=1):
        self.address = address
        self.bus = smbus.SMBus(bus_number)

    def write(self, data):
        self.bus.write_byte(self.address, data)

    def read(self):
        return self.bus.read_byte(self.address)

    def get_pin(self, pin):
        value = self.read()
        return (value >> pin) & 1

    def toggle_pin(self, pin):
        current_state = self.read()
        new_state = current_state ^ (1 << pin)
        self.write(new_state)
        return self.get_pin(pin)

# Initialize the PCF8574 to the correct I2C address
address = 0x27  # Example address, change if different
pcf8574 = PCF8574(address)

# Test each pin
for pin in range(9):  # Assuming 8 pins
    print(f'Testing pin {pin}')
    current_state = pcf8574.toggle_pin(pin)
    print(f'Pin {pin} is now {"on" if current_state == 1 else "off"}')
    time.sleep(2)  # Time to observe the relay
    pcf8574.toggle_pin(pin)  # Turn it off again
    time.sleep(1)
