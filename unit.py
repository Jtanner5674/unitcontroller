from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403
import json

app = Flask(__name__)

dac_objects = {}
dac_addresses = {}

        #Scan for the DACS
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

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', dac_objects=dac_objects)

@app.route('/settings')
def settings():
    return render_template('config/index.html')


def set_voltage_action(dac_id, channel, value):
    addr = dac_addresses.get(dac_id)
    dac = DFRobot_GP8403.DFRobot_GP8403(addr)
    if dac:
        channel_num = DFRobot_GP8403.CHANNEL0 if channel == 1 else DFRobot_GP8403.CHANNEL1
        dac.set_DAC_out_voltage(value, channel_num)
        return jsonify({'message': f'Voltage set to {value}V for Channel {channel_num} on address {hex(addr)} with id {dac_id}'})
    else:
        return jsonify({'error': 'Invalid DAC ID'})

@app.route('/set_voltage<int:dac_id>', methods=['POST'])
def set_voltage1(dac_id):
    voltage = float(request.form['voltage1'])
    return set_voltage_action(dac_id, 1, voltage)

@app.route('/set_voltage2<int:dac_id>', methods=['POST'])
def set_voltage2(dac_id):
    voltage = float(request.form['voltage2'])
    return set_voltage_action(dac_id, 2, voltage)

@app.route('/close1<int:dac_id>', methods=['POST'])
def close1(dac_id):
    return set_voltage_action(dac_id, 1, 2000)

@app.route('/close2<int:dac_id>', methods=['POST'])
def close2(dac_id):
    return set_voltage_action(dac_id, 2, 2000)

@app.route('/open1<int:dac_id>', methods=['POST'])
def open1(dac_id):
    return set_voltage_action(dac_id, 1, 10000)

@app.route('/open2<int:dac_id>', methods=['POST'])
def open2(dac_id):
    return set_voltage_action(dac_id, 2, 10000)


# Function to load JSON data from a file
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Route to get the entire configuration
@app.route('/config', methods=['GET'])
def get_dac_config():
    existing_configs = load_config()
    return jsonify({'dac_addresses': dac_addresses, 'existing_configs': existing_configs})


# Function to save JSON data to a file
def save_config(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=2)

# Route to serve HTML form for updating configuration
@app.route('/update_config/<string:section>/<int:index>', methods=['GET'])
def update_config_form(section, index):
    return render_template('update_config.html', section=section, index=index)

# Route to update a specific configuration item
@app.route('/config/<string:section>/<int:index>', methods=['PUT'])
def update_config(section, index):
    data = load_config()
    new_value = request.json  # New value from the request
    data[section][index] = new_value  # Update the specified item
    save_config(data)  # Save updated data to the file
    return jsonify(data[section][index])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)