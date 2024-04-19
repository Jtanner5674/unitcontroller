import smbus

class RelayController:
    def __init__(self, address, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.current_status = 0b00000000  # Assume all relays are initially off

    def _send_update(self):
        self.bus.write_byte(self.address, self.current_status)

    def on(self, *relays):
        if not relays:  # If no relay number is provided, turn all on
            self.current_status = 0b11111111
        else:
            for relay in relays:
                self.current_status |= (1 << (relay - 1))
        self._send_update()

    def off(self, *relays):
        if not relays:  # If no relay number is provided, turn all off
            self.current_status = 0b00000000
        else:
            for relay in relays:
                self.current_status &= ~(1 << (relay - 1))
        self._send_update()

# Example usage:
# Create an instance of the RelayController
#relay = RelayController(bus_number=1, address=0x27)

# Interface methods
#relay.on(1)     # Turn on relay 1
#relay.off(3)    # Turn off relay 3
#relay.on(1, 4)  # Turn on relay 1 and 4
#relay.off()     # Turn off all relays
#relay.on()      # Turn on all relays
