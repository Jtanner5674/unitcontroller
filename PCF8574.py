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

    def write_pattern(self, pattern):
        """Write a binary pattern to the PCF8574."""
        # Convert binary string to integer
        data = int(pattern, 2)
        self.write(data)

    def get_pin(self, pin):
        """Get the status of a single pin."""
        value = self.read()
        return (value >> pin) & 1

def main():
    address = int(input("Enter the I2C address of the PCF8574: "), 16)  # Prompt user for the I2C address
    expander = PCF8574(address)

    while True:
        print("\nMenu:")
        print("1. Write Bit Pattern")
        print("2. Read All Pins")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            pattern = input("Enter 8-bit pattern (e.g., 00000000 for all low): ")
            expander.write_pattern(pattern)
            print(f"Pattern {pattern} written to PCF8574")
        elif choice == '2':
            value = expander.read()
            bin_value = format(value, '08b')
            print(f"Current state of all pins: {bin_value}")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
