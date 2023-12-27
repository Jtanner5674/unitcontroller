from flask import Flask, render_template, request, jsonify
import board
import busio
import DFRobot_GP8403  # Import the DFRobot_GP8403 library

app = Flask(__name__)

found_dacs = {}

# Define the hexadecimal addresses for DACs
dac_addresses = [0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F]

# Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

try:
    print("Checking I2C bus...")
    for addr in dac_addresses:
        if addr in i2c.scan():
            dac = DFRobot_GP8403.DFRobot_GP8403(addr, i2c)
            found_dacs[addr] = {
                'Channel0': 0,
                'Channel1': 0
            }
            print(f"DAC found at address {hex(addr)} on the valid I2C bus.")
except Exception as e:
    print("Error while initializing DAC:", e)


# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', found_dacs=found_dacs)

@app.route('/get_current_voltages', methods=['GET'])
def get_current_voltages():
    voltages = {}
    for addr, dac in found_dacs.items():
        voltages[hex(addr)] = {
            'Channel0': dac.read_DAC_out_voltage(DFRobot_GP8403.CHANNEL0),
            'Channel1': dac.read_DAC_out_voltage(DFRobot_GP8403.CHANNEL1)
        }
    return jsonify(voltages)
    
@app.route('/set_voltage<int:dac_address>', methods=['POST'])
def set_voltage(dac_address):
    voltage = float(request.form[f'voltage{dac_address}'])
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)
    return f'Voltage set to {voltage}V for Channel 0 on DAC {dac_address}'

@app.route('/closed<int:dac_address>')
def set_closed(dac_address):
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
    return f'Closed Channel 0 on DAC {dac_address}'

@app.route('/open<int:dac_address>')
def set_open(dac_address):
    for dac in found_dacs:
        if dac.address == dac_address:
            dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL0)
    return f'Opened Channel 0 on DAC {dac_address}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)