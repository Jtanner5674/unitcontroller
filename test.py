import unittest
import time
from RelayController import RelayController

class TestRelayController(unittest.TestCase):
    def setUp(self):
        self.relay = RelayController(address=0x27)

    def test_all_relays_on(self):
        self.relay.on()
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b00000000, "All relays should now be on.")

    def test_relay_on(self):
        self.relay.on(2)
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b11111011, "Relay 2 should now be on.")

    def test_relay_off(self):
        self.relay.on(1)  # Turn relay 1 on before turning it off
        time.sleep(1)
        self.relay.off(1)
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b11111111, "Relay 1 should now be off.")

    def test_multiple_relays_on(self):
        self.relay.on(1, 3)
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b11110101, "Relays 1 and 3 should now be on.")

    def test_relay_state_persistence(self):
        self.relay.off()  # Turn all relays off initially
        time.sleep(1)
        self.relay.on(2)  # Turn relay 2 on
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b11111011, "Relay 2 should now be on and others off.")
        self.relay.on(1)  # Then turn relay 1 on as well
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b11111010, "Relays 1 and 2 should now be on and others off.")
        self.relay.off(1)  # Then turn relay 1 off
        time.sleep(1)
        self.assertEqual(self.relay.current_status, 0b11111110, "Relay 1 should now be off, and Relay 2 should still be on.")

    def tearDown(self):
        self.relay.off()  # Turn off all relays after tests

if __name__ == '__main__':
    unittest.main()
