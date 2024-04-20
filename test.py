import unittest
from unittest.mock import MagicMock
from RelayModule import RelayController  # Ensure you import RelayController from the correct location

class TestRelayController(unittest.TestCase):
    def setUp(self):
        # Mock the SMBus method calls
        smbus_mock = MagicMock()
        self.pcf8574 = MagicMock()
        self.pcf8574.write_byte = MagicMock()

        # Patch the SMBus constructor to return the mock
        patcher = unittest.mock.patch('smbus.SMBus', return_value=smbus_mock)
        self.addCleanup(patcher.stop)
        patcher.start()

        # Create an instance of the RelayController
        self.controller = RelayController(address=0x27)

    def test_all_relays_on(self):
        """Test turning all relays on."""
        self.controller.on()
        self.controller.expander.write.assert_called_once_with(0x00)

    def test_all_relays_off(self):
        """Test turning all relays off."""
        self.controller.off()
        self.controller.expander.write.assert_called_once_with(0xFF)

    def test_relay_on(self):
        """Test turning a single relay on."""
        self.controller.on(2)
        self.controller.expander.write.assert_called_once_with(0xFD)  # 11111101 in binary

    def test_relay_off(self):
        """Test turning a single relay off."""
        self.controller.off(1)
        self.controller.expander.write.assert_called_once_with(0xFF)  # 11111111 in binary

if __name__ == '__main__':
    unittest.main()
