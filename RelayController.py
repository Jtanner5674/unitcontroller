import smbus
import unittest

class RelayController:
    def __init__(self):
        self.current_status = 0b11111111  # All relays off

    def on(self, *relays):
        for relay in relays:
            self.current_status &= ~(1 << (relay - 1))

    def off(self, *relays):
        for relay in relays:
            self.current_status |= (1 << (relay - 1))

class TestRelayController(unittest.TestCase):
    def test_relay_bit_operations(self):
        rc = RelayController()
        
        # Test turning all relays on
        rc.on(1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual(rc.current_status, 0b00000000, "All relays should be on")
        
        # Test turning all relays off
        rc.off(1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual(rc.current_status, 0b11111111, "All relays should be off")
        
        # Test turning one relay on
        rc.off()  # Reset to all relays off
        rc.on(2)
        self.assertEqual(rc.current_status, 0b11111011, "Relay 2 should be on")
        
        # Test turning one relay off
        rc.on()  # Reset to all relays on
        rc.off(2)
        self.assertEqual(rc.current_status, 0b11111110, "Relay 2 should be off")
        
        # Test multiple relays on
        rc.off()  # Reset to all relays off
        rc.on(2, 4)
        self.assertEqual(rc.current_status, 0b11101011, "Relays 2 and 4 should be on")
        
        # Test multiple relays off
        rc.on()  # Reset to all relays on
        rc.off(2, 4)
        self.assertEqual(rc.current_status, 0b11111100, "Relays 2 and 4 should be off")
        
if __name__ == '__main__':
    unittest.main()
