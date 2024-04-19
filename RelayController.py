import smbus

class RelayController:
    def __init__(self, address, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.current_status = 0b00000000  # Start with all relays off

    def _send_update(self):
        # Make sure current_status is always a byte when sending to hardware
        self.bus.write_byte(self.address, self.current_status & 0xFF)

    def on(self, *relays):
        if not relays:  # Turn all relays on if no specific relay is provided
            self.current_status = 0xFF
        else:
            for relay in relays:
                self.current_status |= (1 << (relay - 1))
        self._send_update()

    def off(self, *relays):
        if not relays:  # Turn all relays off if no specific relay is provided
            self.current_status = 0x00
        else:
            for relay in relays:
                self.current_status &= ~(1 << (relay - 1))
        self._send_update()

# Example usage:
# relay_controller = RelayController(address=0x27)
# relay_controller.on(1)  # Turns on relay 1
# relay_controller.off(2)  # Turns off relay 2
# relay_controller.on()    # Turns all relays on
# relay_controller.off()   # Turns all relays off
