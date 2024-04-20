from RelayController import RelayController

def test_relay_operations(controller):
    # Ensure all relays are off initially
    controller.off()
    assert controller.state == 0xFF, "Failed to initialize with all relays off."
    print("Initialization test passed: All relays are off.")

    # Test turning on each relay individually
    for i in range(1, 5):
        controller.on(i)
        expected_state = 0xFF & ~(1 << (i - 1))
        assert controller.state == expected_state, f"Failed to turn on relay {i}."
        print(f"Test passed: Relay {i} is on.")

    # Test turning off each relay individually
    for i in range(1, 5):
        controller.off(i)
        expected_state = 0xFF | (1 << (i - 1))
        assert controller.state == expected_state, f"Failed to turn off relay {i}."
        print(f"Test passed: Relay {i} is off.")

    # Test turning on all relays at once
    controller.on()
    assert controller.state == 0x00, "Failed to turn all relays on."
    print("Test passed: All relays are on.")

    # Test turning off all relays at once
    controller.off()
    assert controller.state == 0xFF, "Failed to turn all relays off."
    print("Test passed: All relays are off.")

    print("All tests passed.")

# Main test execution
if __name__ == "__main__":
    # Replace with the actual I2C address of your relay module
    address = 0x27
    relay_controller = RelayController(address)
    test_relay_operations(relay_controller)



#Relay Control Functions:
# __init__(address, bus_number=1): 
# on(*relays): Turns on the specified relay(s). If no relay numbers are provided, all relays are turned on.
# off(*relays): Turns off the specified relay(s). If no relay numbers are provided, all relays are turned off.
# toggle(relay): Toggles the specified relay. If it's on, it will be turned off, and vice versa.
# get_state(): Returns the current state of all relays as a binary string.