import smbus

class RelayController:
    def __init__(self, address, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.current_status = 0b11111111  # Start with all relays off

    def _send_update(self):
        # Directly send the current_status byte to the hardware
        self.bus.write_byte(self.address, self.current_status)

    def on(self, *relays):
        # Turns specified relays on by setting corresponding bits to 0
        if not relays:
            self.current_status = 0b00000000  # All relays on
        else:
            for relay in relays:
                self.current_status &= ~(1 << (relay - 1))
        self._send_update()

    def off(self, *relays):
        # Turns specified relays off by setting corresponding bits to 1
        if not relays:
            self.current_status = 0b11111111  # All relays off
        else:
            for relay in relays:
                self.current_status |= (1 << (relay - 1))
        self._send_update()

# Example usage
# relay_controller = RelayController(address=0x27)
# relay_controller.on(1)  # Turns on relay 1
# relay_controller.off(2)  # Turns off relay 2
# relay_controller.on()    # Turns all relays on
# relay_controller.off()   # Turns all relays off
