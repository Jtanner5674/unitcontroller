import smbus
import time


# Interface methods
relay = RelayController(bus_number=1, address=0x27)
relay.on(1)     # Turn on relay 1
time.sleep(1)
relay.off(3)    # Turn off relay 3
time.sleep(1)
relay.on(1, 4)  # Turn on relay 1 and 4
time.sleep(1)
relay.off()     # Turn off all relays
time.sleep(1)
relay.on()      # Turn on all relays
