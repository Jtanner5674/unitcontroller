import busio
import board
import DFRobot_GP8403
import time

try:
    # Initialize the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    dac = DFRobot_GP8403.DFRobot_GP8403(0x5e)
    dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
    dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL0)
    dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL1)
except Exception as e:
    print("Error while initializing DAC:", e)

voltage = 2000 
x = 1
while x == 1:  # Correct the while loop syntax
    for _ in range(8):
        voltage += 1000
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL1)
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)
        print(f"Voltage: {voltage}")
        time.sleep(11)

    for _ in range(8):
        voltage -= 1000
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL1)
        print(f"Voltage: {voltage}")
        time.sleep(11)
