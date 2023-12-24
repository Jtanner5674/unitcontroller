from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403

app = Flask(__name__)

found_dacs = []

# Define the hexadecimal addresses for DACs
dac_addresses = [0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F]

# Scan for valid I2C buses and DACs
ALL_I2C = (board.I2C(), board.STEMMA_I2C(), busio.I2C(board.GP1, board.GP0))
for bus in ALL_I2C:
    try:
        print("Checking I2C bus...")
        for addr in dac_addresses:
            bus.scan()
            if addr in bus.scan():
                dac = DFRobot_GP8403.DFRobot_GP8403(addr, i2c=bus)
                dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
                dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
                dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
                found_dacs.append(dac)
                print(f"DAC found at address {hex(addr)} on the valid I2C bus.")
    except Exception as e:
        print("Invalid bus:", e)

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', found_dacs=found_dacs)

@app.route('/get_current_voltages', methods=['GET'])
def get_current_voltages():
    voltages = {}
    for dac in found_dacs
        voltage1 = dac.read_DAC_out_voltage(DFRobot_GP8403.CHANNEL0)
        voltage2 = dac.read_DAC_out_voltage(DFRobot_GP8403.CHANNEL1)
        voltages[f'voltage{dac.address}'] = voltage1
        voltages[f'voltage{dac.address}_ch1'] = voltage2
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