from DFRobot_GP8302 import DFRobot_GP8302
import time

# Initialize the module
module = DFRobot_GP8302()

# Begin communication and initialize the module
status = module.begin()

# Check if initialization was successful
if status != 0:
    print("Initialization failed. Error code:", status)
    # Handle the error as needed

def measure_current_and_get_dac(value):
    while True:
        input("Press Enter when ready to measure {} current (ensure multimeter is connected)...".format(value))
        # Measure the current using a multimeter and input the measured value
        dac = module.output(current_mA = value)
        measured_current = float(input("Enter the measured current (mA) for {} current: ".format(value)))
        # Calculate the DAC value
        dac_value = int((measured_current / 25) * 4095)
        print("Calculated DAC value for {} current: {}".format(value, dac_value))

        # Ask if the user wants to proceed or re-measure
        choice = input("Do you want to use this value for calibration? (yes/no): ").lower()
        if choice == 'yes':
            return dac_value
        elif choice == 'no':
            continue
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

# Measure and get DAC value for 4mA current
dac_4 = measure_current_and_get_dac(4)

# Measure and get DAC value for 20mA current
dac_20 = measure_current_and_get_dac(20)

# Calibrate the module
module.calibration4_20mA(dac_4=dac_4, dac_20=dac_20)

print("Calibration completed successfully!")
