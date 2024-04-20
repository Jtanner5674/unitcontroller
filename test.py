from RelayController import RelayController
import time

# Change the I2C address to match your hardware setup
RELAY_BOARD_ADDRESS = 0x27  # Example I2C address for PCF8574
DELAY_BETWEEN_TESTS = 2  # Delay in seconds

def test_relay_operations(controller):
    # Test turning each relay on one by one
    for i in range(1, 5):
        print(f"Turning on relay {i}")
        controller.on(i)
        print(f"Current state: {controller.get_state()}")
        time.sleep(DELAY_BETWEEN_TESTS)

    # Test turning each relay off one by one
    for i in range(1, 5):
        print(f"Turning off relay {i}")
        controller.off(i)
        print(f"Current state: {controller.get_state()}")
        time.sleep(DELAY_BETWEEN_TESTS)

    # Test toggling each relay
    for i in range(1, 5):
        print(f"Toggling relay {i}")
        controller.toggle(i)
        print(f"Current state: {controller.get_state()}")
        time.sleep(DELAY_BETWEEN_TESTS)
        controller.toggle(i)  # Toggle back to original state

    # Test turning all relays on and then off
    print("Turning all relays on")
    controller.on()
    print(f"Current state: {controller.get_state()}")
    time.sleep(DELAY_BETWEEN_TESTS)

    print("Turning all relays off")
    controller.off()
    print(f"Current state: {controller.get_state()}")
    time.sleep(DELAY_BETWEEN_TESTS)


def main():
    relay_controller = RelayController(RELAY_BOARD_ADDRESS)
    test_relay_operations(relay_controller)


if __name__ == "__main__":
    main()



#Relay Control Functions:
# __init__(address, bus_number=1): 
# on(*relays): Turns on the specified relay(s). If no relay numbers are provided, all relays are turned on.
# off(*relays): Turns off the specified relay(s). If no relay numbers are provided, all relays are turned off.
# toggle(relay): Toggles the specified relay. If it's on, it will be turned off, and vice versa.
# get_state(): Returns the current state of all relays as a binary string.