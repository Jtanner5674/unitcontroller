from PCF8574 import PCF8574
from time import sleep

class RelayController(PCF8574):
    def __init__(self, address, bus_number=1):
        super().__init__(address, bus_number)
        self.state = 0xFF  # All relays are off initially (0b11111111)
        self.write(self.state)  # Ensure initial state is set

    def on(self, *relays):
        if not relays:
            self.state &= 0x0F
        else:
            for relay in relays:
                if 1 <= relay <= 4:
                    self.state &= ~(0x80 >> (relay - 1))
                else:
                    raise ValueError("Relay number must be between 1 and 4")
        self.write(self.state)

    def off(self, *relays):
        if not relays:
            self.state |= 0xF0
        else:
            for relay in relays:
                if 1 <= relay <= 4:
                    self.state |= (0x80 >> (relay - 1))
                else:
                    raise ValueError("Relay number must be between 1 and 4")
        self.write(self.state)

    def toggle(self, relay):
        if 1 <= relay <= 4:
            self.state ^= (0x80 >> (relay - 1))
            self.write(self.state)
        else:
            raise ValueError("Relay number must be between 1 and 4")

    def get_state(self):
        return bin(self.state & 0xF0)

    def enginestarter(self, live, starter, start_time=2):
        self.on(live, starter) 
        sleep(start_time)  # Ensure there is a delay for the starter to engage properly
        self.off(starter)
        self.state = self.get_state()
        self.state = int(self.state, 2) + live  # Convert the binary string to an integer before addition
        self.write(self.state) 