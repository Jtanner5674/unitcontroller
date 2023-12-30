from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403

app = Flask(__name__)

found_dacs = []

# Define the hexadecimal addresses for DACs
dac_addresses = [0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F]

try:
    # Initialize the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Checking I2C bus...")
    for addr in dac_addresses:
        if addr in i2c.scan():
            # Initialize the DAC without passing 'i2c'
            dac = DFRobot_GP8403.DFRobot_GP8403(addr)
            dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
            found_dacs.append(dac)
            print(f"DAC found at address {hex(addr)} on the valid I2C bus.")
except Exception as e:
    print("Error while initializing DAC:", e)

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', found_dac_addresses=found_dac_addresses)

@app.route('/set_voltage1<int:dac_address>', methods=['POST'])
def set_voltage1(dac_address):
    global percentage1  # Declare the variable as global

    percentage = float(request.form['voltage1'])
    percentage1 = percentage  # Set the global variable to the received percentage
    voltage = 2 + (percentage / 100) * 8  # Convert percentage to the 2-10 range
    dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)  # Set voltage on channel 1
    return f'Voltage set to {voltage}V for Channel 1'

@app.route('/set_voltage2<int:dac_address>', methods=['POST'])
def set_voltage2(dac_address):
    global percentage2  # Declare the variable as global

    percentage = float(request.form['voltage2'])
    percentage2 = percentage  # Set the global variable to the received percentage
    voltage = 2 + (percentage / 100) * 8  # Convert percentage to the 2-10 range
    dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL1)  # Set voltage on channel 2
    return f'Voltage set to {voltage}V for Channel 2'

@app.route('/close1<int:dac_address>')
def close1(dac_address):
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
    return f'Closed Channel 0 on DAC {dac_address}'

@app.route('/close2<int:dac_address>')
def close2(dac_address):
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
    return f'Closed Channel 1 on DAC {dac_address}'

@app.route('/open1<int:dac_address>')
def open1(dac_address):
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL0)
    return f'Opened Channel 0 on DAC {dac_address}'

@app.route('/open2<int:dac_address>')
def open2(dac_address):
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL1)
    return f'Opened Channel 1 on DAC {dac_address}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)