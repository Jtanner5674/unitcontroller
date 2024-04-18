import smbus

# Create an instance of the I2C bus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# I2C address of the device
address = 0x27

# Data to send (0b11111111, which is 255 in decimal)
data = 0b11111111

# Sending the data
bus.write_byte(address, data)
