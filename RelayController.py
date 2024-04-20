import smbus

class RelayController:
    def __init__(self, address, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        # Start with all relays off (1 = OFF, 0 = ON)
        self.current_status = 0b11111111

    def _send_update(self):
        # Send the full byte to the hardware
        self.bus.write_byte(self.address, self.current_status)

    def on(self, *relays):
        # Turns specified relays on by setting corresponding bits to 0
        if not relays:
            # If no relay numbers are provided, turn all relays on
            self.current_status = 0b00000000
        else:
            for relay in relays:
                # Bitwise AND with the complement of the bit mask to turn on relay
                self.current_status &= ~(1 << (relay - 1))
        self._send_update()

    def off(self, *relays):
        # Turns specified relays off by setting corresponding bits to 1
        if not relays:
            # If no relay numbers are provided, turn all relays off
            self.current_status = 0b11111111
        else:
            for relay in relays:
                # Bitwise OR with the bit mask to turn off relay
                self.current_status |= (1 << (relay - 1))
        self._send_update()

# Example usage
# relay_controller = RelayController(address=0x27)
# relay_controller.on(1)  # Turns on relay 1
# relay_controller.off(2)  # Turns off relay 2
# relay_controller.on()    # Turns all relays on
# relay_controller.off()   # Turns all relays off
