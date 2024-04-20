from RelayModule import RelayController 

def test_relay_operations(controller):
    # Test turning on each relay individually
    for i in range(1, 5):
        controller.off()  # Ensure all relays are off
        controller.on(i)
        assert controller.state == 0xFF ^ (1 << (i - 1)), f"Relay {i} failed to turn on."
        print(f"Relay {i} on test passed.")

    # Test turning off each relay individually
    for i in range(1, 5):
        controller.on()  # Ensure all relays are on
        controller.off(i)
        assert controller.state == 0x00 | (1 << (i - 1)), f"Relay {i} failed to turn off."
        print(f"Relay {i} off test passed.")

    # Test turning on all relays at once
    controller.off()  # Ensure all relays are off
    controller.on()
    assert controller.state == 0x00, "All relays failed to turn on."
    print("All on test passed.")

    # Test turning off all relays at once
    controller.on()  # Ensure all relays are on
    controller.off()
    assert controller.state == 0xFF, "All relays failed to turn off."
    print("All off test passed.")

    print("All tests passed.")

# Main test execution
if __name__ == "__main__":
    # Assuming the device address is 0x27; replace with the actual address of your device.
    controller = RelayController(address=0x27)
    
    test_relay_operations(controller)
