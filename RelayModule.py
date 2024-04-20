import PCF8574

class RelayController:
    def __init__(self, address, bus_number=1):
        self.expander = PCF8574.PCF8574(address, bus_number)
        self.relay_states = 0xFF  # All relays off (1 means off in this context)

    def on(self, relay_number=None):
        """Turns a specific relay or all relays ON. If no relay number is provided, turns all relays ON."""
        if relay_number is None:
            self.relay_states = 0x00
        else:
            self.relay_states &= ~(1 << (relay_number - 1))
        self.update_relays()

    def off(self, relay_number=None):
        """Turns a specific relay or all relays OFF. If no relay number is provided, turns all relays OFF."""
        if relay_number is None:
            self.relay_states = 0xFF
        else:
            self.relay_states |= (1 << (relay_number - 1))
        self.update_relays()

    def update_relays(self):
        """Update the relay module with the current states."""
        self.expander.write(self.relay_states)
