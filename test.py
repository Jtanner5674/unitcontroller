import unittest
from RelayController import RelayController  # Make sure to replace 'your_relay_library' with the actual name of your Python file containing the RelayController class.

class TestRelayController(unittest.TestCase):
    def setUp(self):
        # Initialize the RelayController with a typical I2C address
        self.relay = RelayController(address=0x27)

    def test_all_relays_off(self):
        """Test that all relays can be turned off."""
        self.relay.all_relays_off()
        # This test assumes there is a method to read back relay states which does not exist in the current implementation
        # This would need hardware support to be fully testable
        print("All relays should now be off.")

    def test_relay_on(self):
        """Test turning a single relay on."""
        self.relay.relay_on(2)
        # Similarly, we assume to have a feedback mechanism to confirm relay states
        print("Relay 2 should now be on.")

    def test_relay_off(self):
        """Test turning a single relay off."""
        self.relay.relay_on(1)  # Ensure relay 1 is on before testing off
        self.relay.relay_off(1)
        print("Relay 1 should now be off.")

    def test_multiple_relays_on(self):
        """Test turning multiple relays on."""
        self.relay.control_multiple_relays([1, 3], True)
        print("Relays 1 and 3 should now be on.")

    def test_relay_state_persistence(self):
        """Test if turning one relay on affects the other."""
        self.relay.all_relays_off()
        self.relay.relay_on(1)
        self.relay.relay_on(2)
        self.relay.relay_off(1)
        print("Relay 1 should now be off, and Relay 2 should still be on.")

    def tearDown(self):
        """Cleanup actions after each test."""
        self.relay.all_relays_off()  # Turn off all relays after tests
        self.relay.close()

if __name__ == '__main__':
    unittest.main()
