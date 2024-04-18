import smbus
import time

class RelayController:
    def __init__(self, address=0x27, bus_number=1):
        self.address = address
        self.bus = smbus.SMBus(bus_number)

    def all_relays_off(self):
        """Turns all relays off."""
        self.bus.write_byte(self.address, 0b11111111)

    def relay_on(self, relay_number):
        """Turns a specific relay on. Relays are numbered 1-4."""
        if 1 <= relay_number <= 4:
            mask = 0b11111111 ^ (1 << (relay_number - 1))
            self.bus.write_byte(self.address, mask)

    def relay_off(self, relay_number):
        """Turns a specific relay off. Relays are numbered 1-4."""
        if 1 <= relay_number <= 4:
            mask = 0b11111111 | (1 << (relay_number - 1))
            self.bus.write_byte(self.address, mask)

    def control_multiple_relays(self, relays, state):
        """
        Controls multiple relays.
        :param relays: List of relay numbers (1-4)
        :param state: True to turn on, False to turn off
        """
        current_state = 0b11111111
        for relay in relays:
            if 1 <= relay <= 4:
                if state:
                    current_state &= ~(1 << (relay - 1))
                else:
                    current_state |= (1 << (relay - 1))
        self.bus.write_byte(self.address, current_state)

    def close(self):
        """Closes the bus connection."""
        self.bus.close()
