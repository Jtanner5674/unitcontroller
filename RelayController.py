from PCF8574 import PCF8574

class RelayController(PCF8574):
    def __init__(self, address, bus_number=1):
        super().__init__(address, bus_number)
        self.state = 0xFF  # All relays are off initially (0b11111111)
        self.write(self.state)  # Ensure initial state is set

    def on(self, *relays):
        if not relays:
            # Turn the first four relays on (set the first four bits to 0)
            self.state &= 0x0F
        else:
            for relay in relays:
                if 1 <= relay <= 4:
                    # Set the bit corresponding to the relay to 0
                    self.state &= ~(0x80 >> (relay - 1))
                else:
                    raise ValueError("Relay number must be between 1 and 4")
        self.write(self.state)

    def off(self, *relays):
        if not relays:
            # Turn the first four relays off (set the first four bits to 1)
            self.state |= 0xF0
        else:
            for relay in relays:
                if 1 <= relay <= 4:
                    # Set the bit corresponding to the relay to 1
                    self.state |= (0x80 >> (relay - 1))
                else:
                    raise ValueError("Relay number must be between 1 and 4")
        self.write(self.state)

    def toggle(self, relay):
        if 1 <= relay <= 4:
            # Toggle the bit corresponding to the relay
            self.state ^= (0x80 >> (relay - 1))
            self.write(self.state)
        else:
            raise ValueError("Relay number must be between 1 and 4")

    def get_state(self):
        # Return the current state of all relays with the first four bits
        return bin(self.state & 0xF0)

