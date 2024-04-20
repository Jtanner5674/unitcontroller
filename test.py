import unittest
from unittest.mock import MagicMock, patch
from RelayModule import RelayController  # Adjust this import path as needed

class TestRelayController(unittest.TestCase):
    def setUp(self):
        # Patch the SMBus class in the PCF8574 module
        patcher = patch('PCF8574.smbus.SMBus')
        self.MockSMBus = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock the SMBus instance and its methods
        self.mock_bus = MagicMock()
        self.MockSMBus.return_value = self.mock_bus
        
        # Create an instance of the RelayController
        self.controller = RelayController(address=0x27)
        self.controller.expander.bus = self.mock_bus  # Replace the SMBus instance with the mock

    def test_all_relays_on(self):
        """Test turning all relays on."""
        self.controller.on()
        self.mock_bus.write_byte.assert_called_once_with(0x27, 0x00)

    def test_all_relays_off(self):
        """Test turning all relays off."""
        self.controller.off()
        self.mock_bus.write_byte.assert_called_once_with(0x27, 0xFF)

    def test_relay_on(self):
        """Test turning a single relay on."""
        self.controller.on(2)
        expected_value = 0xFF & ~(1 << (2 - 1))
        self.mock_bus.write_byte.assert_called_once_with(0x27, expected_value)

    def test_relay_off(self):
        """Test turning a single relay off."""
        self.controller.off(1)
        expected_value = 0xFF | (1 << (1 - 1))
        self.mock_bus.write_byte.assert_called_once_with(0x27, expected_value)

if __name__ == '__main__':
    unittest.main()
s