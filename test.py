from PCF8574 import PCF8574

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
