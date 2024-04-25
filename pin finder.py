from RelayController import RelayController
import time

# Initialize the Relay Controller with the correct I2C address
relay_controller = RelayController(address=0x27)

# Try turning on each pin one at a time to see which one controls relay one
for pin in range(8):  # Assuming 8 pins from 0 to 7 for PCF8574
    print(f"Testing pin {pin}")
    relay_controller.on(pin)
    time.sleep(2)  # Wait 2 seconds to observe the relay
    relay_controller.off(pin)
    time.sleep(1)  # Cool down period between tests
