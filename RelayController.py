from PCF8574 import PCF8574

class RelayController(PCF8574):
    def __init__(self, address, bus_number=1):
        super().__init__(address, bus_number)
        self.state = 0xFF  # All relays are off initially (0b11111111)

    def on(self, *relays):
        # If no relay numbers are given, turn all relays on
        if not relays:
            self.state = 0x00
        else:
            for relay in relays:
                if 1 <= relay <= 4:
                    self.state &= ~(1 << (relay - 1))
                else:
                    raise ValueError("Relay number must be between 1 and 4")
        self.write(self.state)

    def off(self, *relays):
        # If no relay numbers are given, turn all relays off
        if not relays:
            self.state = 0xFF
        else:
            for relay in relays:
                if 1 <= relay <= 4:
                    self.state |= (1 << (relay - 1))
                else:
                    raise ValueError("Relay number must be between 1 and 4")
        self.write(self.state)

    def toggle(self, relay):
        """Toggle the specified relay."""
        if 1 <= relay <= 4:
            self.state ^= (1 << (relay - 1))
            self.write(self.state)
        else:
            raise ValueError("Relay number must be between 1 and 4")

    def get_state(self):
        """Return the current state of all relays."""
        return bin(self.state)
