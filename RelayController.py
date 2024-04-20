import smbus

class RelayController:
    def __init__(self, address, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        # Start with all relays off (all bits set to 1), represented as a string for clarity
        self.current_status = '11111111'

    def _send_update(self):
        # Convert the binary string back to an integer to send to hardware
        status_to_send = int(self.current_status, 2)
        print(f"Updating relays with status: {self.current_status} (binary) -> {status_to_send:#010b} (to send)")
        self.bus.write_byte(self.address, status_to_send)

    def on(self, *relays):
        if not relays:  # Turn all relays on if no specific relay is provided
            self.current_status = '00000000'
        else:
            status_list = list(self.current_status)
            for relay in relays:
                # Insert '0' at the correct index to turn the relay on
                status_list[-relay] = '0'
                self.current_status = ''.join(status_list)
        self._send_update()

    def off(self, *relays):
        if not relays:  # Turn all relays off if no specific relay is provided
            self.current_status = '11111111'
        else:
            status_list = list(self.current_status)
            for relay in relays:
                # Insert '1' at the correct index to turn the relay off
                status_list[-relay] = '1'
                self.current_status = ''.join(status_list)
        self._send_update()

# Example usage:
relay_controller = RelayController(address=0x27)
relay_controller.on(1)  # Turns on relay 1 (0b01111111)
relay_controller.off(2)  # Turns off relay 2 (0b11111111)
relay_controller.on()    # Turns all relays on (0b00000000)
relay_controller.off()   # Turns all relays off (0b11111111)
