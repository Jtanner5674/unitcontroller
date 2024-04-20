class RelayController:
    def __init__(self):
        self.current_status = 0b11111111  # All relays off

    def on(self, *relays):
        for relay in relays:
            # Ensure that relay 1 corresponds to the first (LSB) bit
            self.current_status &= ~(1 << (relay - 1))

    def off(self, *relays):
        for relay in relays:
            # Ensure that relay 1 corresponds to the first (LSB) bit
            self.current_status |= (1 << (relay - 1))

class TestRelayController(unittest.TestCase):
    def test_relay_bit_operations(self):
        rc = RelayController()
        
        # Turn relay 2 on and check
        rc.on(2)
        expected_status_on = 0b11111011  # Binary representation of all relays off except for relay 2
        self.assertEqual(rc.current_status, expected_status_on, f"Relay 2 should be on, got {bin(rc.current_status)} instead of {bin(expected_status_on)}")
        
        # Reset and turn relay 2 off and check
        rc.current_status = 0b11111111  # Reset to all relays off
        rc.off(2)
        expected_status_off = 0b11111111  # Binary representation of all relays off including relay 2
        self.assertEqual(rc.current_status, expected_status_off, f"Relay 2 should be off, got {bin(rc.current_status)} instead of {bin(expected_status_off)}")

if __name__ == '__main__':
    unittest.main()
