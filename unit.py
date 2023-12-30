from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403

app = Flask(__name__)

dac_objects = {}  # Dictionary to store DAC objects with IDs

# Define the hexadecimal addresses for DACs
dac_addresses = [0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F]

try:
    # Initialize the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Checking I2C bus...")
    for index, addr in enumerate(dac_addresses):
        if addr in i2c.scan():
            # Initialize the DAC without passing 'i2c'
            dac = DFRobot_GP8403.DFRobot_GP8403(addr)
            dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
            dac_objects[index] = dac  # Store DAC object with ID
            print(f"DAC found at address {hex(addr)} on the valid I2C bus with ID {index}.")
except Exception as e:
    print("Error while initializing DAC:", e)

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', dac_objects=dac_objects)


@app.route('/set_voltage<int:dac_id>', methods=['POST'])
def set_voltage(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        percentage = float(request.form['voltage1'])
        voltage = 2 + (percentage / 100) * 8
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)
        return f'Voltage set to {voltage}V for Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/set_voltage2<int:dac_id>', methods=['POST'])
def set_voltage2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        percentage = float(request.form['voltage2'])
        voltage = 2 + (percentage / 100) * 8
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL1)
        return f'Voltage set to {voltage}V for Channel 2 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/close1<int:dac_id>')
def close1(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
        return f'Closed Channel 0 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/close2<int:dac_id>')
def close2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
        return f'Closed Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/open1<int:dac_id>')
def open1(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL0)
        return f'Opened Channel 0 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/open2<int:dac_id>')
def open2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL1)
        return f'Opened Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)