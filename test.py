import unittest
import time
from RelayController import RelayController

class TestRelayController(unittest.TestCase):
    def setUp(self):
        # Initialize the RelayController with a typical I2C address
        self.relay = RelayController(address=0x27)

    def test_all_relays_on(self):
        """Test that all relays can be turned on."""
        self.relay.on()  # Turns all relays on
        time.sleep(5)  # Wait for 1 second to observe the change
        self.assertEqual(self.relay.current_status, 0xFF, "All relays should now be on.")

    def test_relay_on(self):
        """Test turning a single relay on."""
        self.relay.on(2)
        time.sleep(5)  # Wait for 1 second to observe the relay turning on
        self.assertTrue((self.relay.current_status & (1 << 1)) != 0, "Relay 2 should now be on.")

    def test_relay_off(self):
        """Test turning a single relay off."""
        self.relay.on(1)  # Ensure relay 1 is on before testing off
        time.sleep(5)  # Wait for 1 second to observe the change
        self.relay.off(1)
        time.sleep(5)  # Wait for 1 second to observe the change
        self.assertTrue((self.relay.current_status & (1 << 0)) == 0, "Relay 1 should now be off.")

    def test_multiple_relays_on(self):
        """Test turning multiple relays on."""
        self.relay.on(1, 3)
        time.sleep(5)  # Wait for 1 second to observe the change
        self.assertTrue((self.relay.current_status & (1 << 0)) != 0 and (self.relay.current_status & (1 << 2)) != 0, "Relays 1 and 3 should now be on.")

    def test_relay_state_persistence(self):
        """Test if turning one relay on affects the other."""
        self.relay.off()  # Turn all off initially
        time.sleep(5)  # Wait for 1 second to observe the change
        self.relay.on(1)
        time.sleep(5)  # Wait for 1 second to observe the change
        self.relay.on(2)
        time.sleep(5)  # Wait for 1 second to observe the change
        self.relay.off(1)
        time.sleep(5)  # Wait for 1 second to observe the change
        self.assertTrue((self.relay.current_status & (1 << 1)) != 0 and (self.relay.current_status & (1 << 0)) == 0, "Relay 1 should now be off, and Relay 2 should still be on.")

    def tearDown(self):
        """Cleanup actions after each test."""
        self.relay.off()  # Turn off all relays after tests

if __name__ == '__main__':
    unittest.main()
