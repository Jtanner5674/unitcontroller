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
        # With relays on, current_status should be 0 (0b00000000)
        self.assertEqual(self.relay.current_status, 0b00000000, "All relays should now be on.")
        
    def test_relay_on(self):
        """Test turning a single relay on."""
        self.relay.on(2)
        # Relay #2 on means second bit should be 0 (0b11111011)
        self.assertEqual(self.relay.current_status, 0b11111011, "Relay 2 should now be on.")
        
    def test_relay_off(self):
        """Test turning a single relay off."""
        self.relay.on(1)  # Turn relay 1 on before turning it off
        self.relay.off(1)
        # Turning relay 1 off should revert to all relays off (0b11111111)
        self.assertEqual(self.relay.current_status, 0b11111111, "Relay 1 should now be off.")
        
    def test_multiple_relays_on(self):
        """Test turning multiple relays on."""
        self.relay.on(1, 3)
        # Relays 1 and 3 on should be 0b11110101
        self.assertEqual(self.relay.current_status, 0b11110101, "Relays 1 and 3 should now be on.")
        
    def test_relay_state_persistence(self):
        """Test if turning one relay on affects the other."""
        self.relay.off()  # Turn all off initially
        self.relay.on(1)  # Turn relay 1 on
        self.relay.on(2)  # Turn relay 2 on
        self.relay.off(1)  # Then turn relay 1 off
        # Relay 1 off, Relay 2 on should be 0b11111011
        self.assertEqual(self.relay.current_status, 0b11111011, "Relay 1 should now be off, and Relay 2 should still be on.")

    def tearDown(self):
        """Cleanup actions after each test."""
        self.relay.off()  # Turn off all relays after tests

if __name__ == '__main__':
    unittest.main()
