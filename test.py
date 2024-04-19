import unittest
import time
from RelayController import RelayController

class TestRelayController(unittest.TestCase):
    def setUp(self):
        # Initialize the RelayController with a typical I2C address
        self.relay = RelayController(address=0x27)

    def test_all_relays_off(self):
        """Test that all relays can be turned off."""
        self.relay.all_relays_off()
        time.sleep(1)  # Wait for 1 second to observe the change
        print("All relays should now be off.")

    def test_relay_on(self):
        """Test turning a single relay on."""
        self.relay.relay_on(2)
        time.sleep(1)  # Wait for 1 second to observe the relay turning on
        print("Relay 2 should now be on.")

    def test_relay_off(self):
        """Test turning a single relay off."""
        self.relay.relay_on(1)  # Ensure relay 1 is on before testing off
        time.sleep(1)  # Wait for 1 second to observe the relay turning on
        self.relay.relay_off(1)
        time.sleep(1)  # Wait for 1 second to observe the relay turning off
        print("Relay 1 should now be off.")

    def test_multiple_relays_on(self):
        """Test turning multiple relays on."""
        self.relay.control_multiple_relays([1, 3], True)
        time.sleep(1)  # Wait for 1 second to observe the relays turning on
        print("Relays 1 and 3 should now be on.")

    def test_relay_state_persistence(self):
        """Test if turning one relay on affects the other."""
        self.relay.all_relays_off()
        time.sleep(1)
        self.relay.relay_on(1)
        time.sleep(1)
        self.relay.relay_on(2)
        time.sleep(1)
        self.relay.relay_off(1)
        time.sleep(1)  # Wait to ensure Relay 2 is still on after Relay 1 is off
        print("Relay 1 should now be off, and Relay 2 should still be on.")

    def tearDown(self):
        """Cleanup actions after each test."""
        self.relay.all_relays_off()  # Turn off all relays after tests
        self.relay.close()

if __name__ == '__main__':
    unittest.main()
