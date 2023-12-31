from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403
import os
import json

app = Flask(__name__)

dac_objects = {}
dac_addresses = {}

config_file_path = 'config.json'

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as new_config_file:
        new_config_file.write('{}')
        
#Locate the DACS
try:
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Scanning I2C bus for DACs...")
    index = 0
    for o in range(8, 16):  # Equivalent to the range 8..F in hexadecimal
        addr = 0x50 + o 
        try:
            dac = DFRobot_GP8403.DFRobot_GP8403(addr)
            dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
            dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL0)
            dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL1)
            dac_objects[index] = dac
            dac_addresses[index] = addr
            print(f"DAC found at address {hex(addr)} with ID {index}.")
            index += 1
        except Exception as e:
            print(f"No DAC found at address {hex(addr)}")
            continue
except Exception as e:
    print("Error while scanning for DACs:", e)

# Page initializers

@app.route('/')
def index():
    return render_template('index.html', dac_objects=dac_objects)

@app.route('/settings')
def settings():
    return render_template('settings/index.html')

# Function Routes

@app.route('/getConfig', methods=['GET'])
def get_config():
    try:
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)
            return jsonify(config_data)
    except FileNotFoundError:
        return jsonify({}) 

@app.route('/saveConfig', methods=['POST'])
def save_config():
    try:
        updated_config = request.json  
        with open('config.json', 'w') as config_file:
            json.dump(updated_config, config_file, indent=4)
        return 'Config updated successfully!', 200
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/set_voltage<int:dac_id>', methods=['POST'])
def set_voltage(dac_id):
    addr = dac_addresses.get(dac_id)
    dac = DFRobot_GP8403.DFRobot_GP8403(addr)
    if dac:
        percentage = float(request.form['voltage1'])
        voltage = 2 + (percentage / 100) * 8
        volts = voltage * 500
        dac.set_DAC_out_voltage(volts, DFRobot_GP8403.CHANNEL0)
        errval = f'Voltage set to {voltage}V for Channel 0 on address {hex(addr)} with id {dac_id}'
    else:
        errval = "Invalid DAC ID"
    print (errval)
    return (errval)

@app.route('/set_voltage2<int:dac_id>', methods=['POST'])
def set_voltage2(dac_id):
    addr = dac_addresses.get(dac_id)
    dac = DFRobot_GP8403.DFRobot_GP8403(addr)
    if dac:
        percentage = int(request.form['voltage2'])
        voltage = 2 + (percentage / 100) * 8
        volts = voltage * 500
        dac.set_DAC_out_voltage(volts, DFRobot_GP8403.CHANNEL1)
        errval = f'Voltage set to {voltage}V for Channel 1 on address {hex(addr)} with id {dac_id}'
    else:
        errval = "Invalid DAC ID"
    print (errval)
    return (errval)

@app.route('/close1<int:dac_id>')
def close1(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL0)
        return f'Closed Channel 0 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/close2<int:dac_id>')
def close2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL1)
        return f'Closed Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/open1<int:dac_id>')
def open1(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(10000, DFRobot_GP8403.CHANNEL0)
        return f'Opened Channel 0 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/open2<int:dac_id>')
def open2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(10000, DFRobot_GP8403.CHANNEL1)
        return f'Opened Channel 2 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)