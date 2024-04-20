import smbus

class RelayController:
    def __init__(self, address, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.current_status = 0b11111111  # Start with all relays off (all bits set to 1)

    def _send_update(self):
        # Ensure current_status is always a byte when sending to hardware
        self.bus.write_byte(self.address, self.current_status & 0xFF)

    def on(self, *relays):
        if not relays:  # Turn all relays on if no specific relay is provided
            self.current_status = 0b00000000
        else:
            for relay in relays:
                self.current_status &= ~(1 << (relay - 1))  # Set bit to 0 to turn on
        self._send_update()

    def off(self, *relays):
        if not relays:  # Turn all relays off if no specific relay is provided
            self.current_status = 0b11111111
        else:
            for relay in relays:
                self.current_status |= (1 << (relay - 1))  # Set bit to 1 to turn off
        self._send_update()

# Example usage:
# relay_controller = RelayController(address=0x27)
# relay_controller.on(1)  # Turns on relay 1 (bit 0 to 0)
# relay_controller.off(2)  # Turns off relay 2 (bit 1 to 1)
# relay_controller.on()    # Turns all relays on (all bits to 0)
# relay_controller.off()   # Turns all relays off (all bits to 1)
