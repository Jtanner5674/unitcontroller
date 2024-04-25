from flask import Flask, render_template, request, jsonify
import DFRobot_GP8403
import json
import traceback
import busio
import board
import time
from flask_cors import CORS
from RelayController import RelayController

preset_flush_time = 5  # Change this to adjust how long the system flushes in presets
CFG = None
dac_objects = {}
dac_addresses = {}
engine_state = False
############################ Backend Functions ###################################


def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)


def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=2)



def set_voltage_action(addr, percent):
    try:
        volt = int((float(percent) / 100.0) * 10000)
        addr_int = int(addr, 16)
        dac = next(d for d in CFG["dac"] if int(d["id"], 16) == addr_int)
        dac["obj"].set_DAC_out_voltage(volt, DFRobot_GP8403.CHANNEL0)
        dac["obj"].set_DAC_out_voltage(volt, DFRobot_GP8403.CHANNEL1)
        volts = float(volt / 1000)
        dac["current_voltage"] = volt
        print(f'{dac["name"]} set to {volts}V')
        return jsonify({'message': f'{dac["name"]} set to {volts}V'})
    except StopIteration:
        print('error: Invalid DAC ADDR')
        return jsonify({'error': 'Invalid DAC ADDR'})


############################ Initialization ###################################


def initialize_dacs():
    global CFG
    CFG = load_config()  # Ensure this loads a dict with necessary keys
    if "existing_configs" not in CFG:
        CFG["existing_configs"] = {"dac": []}  # Initialize if not present

    global dac_objects
    dac_objects = {}
    # Initialize dac_list directly from CFG, assuming it's always present after load_config
    dac_list = CFG.get("dac", [])

    # Reset 'found' status for existing DAC configs to re-discover them
    for item in dac_list:
        item["found"] = False
        item["current_voltage"] = 0

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        print("Scanning I2C bus for DACs...")
        for addr in range(0x58, 0x60):
            try:
                dac = DFRobot_GP8403.DFRobot_GP8403(addr)
                dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
                dac.set_DAC_out_voltage(0, DFRobot_GP8403.CHANNEL0)
                dac.set_DAC_out_voltage(0, DFRobot_GP8403.CHANNEL1)

                hex_addr = hex(addr)
                found_dac = next(
                    (item for item in dac_list if item["id"] == hex_addr), None)
                if found_dac:
                    found_dac.update({"found": True, "obj": dac})
                else:
                    new_dac = {"name": "New DAC", "id": hex_addr,
                               "found": True, "obj": dac, "current_voltage": 0}
                    dac_list.append(new_dac)

                dac_objects[hex_addr] = new_dac if not found_dac else found_dac
                print(f"DAC found at address {hex_addr}.")
            except Exception as e:
                print(f"No DAC found at address {hex(addr)}")
                continue

        # Update CFG with the newly discovered and existing DACs
        CFG["dac"] = dac_list
        print("DAC configuration after initialization:", CFG)
        return CFG
    except Exception as e:
        print("Error while scanning for DACs:", e)


CFG = initialize_dacs()
app = Flask(__name__)
CORS(app)

############################ Flask Pages ###################################


@app.route('/')
def index():
    existing_configs = load_config()
    return render_template('index.html', dac_objects=dac_objects, dac_addresses=dac_addresses, existing_configs=existing_configs)


@app.route('/settings')
def settings():
    existing_configs = load_config()
    online_dacs = [dac for dac in CFG["dac"] if dac["found"]]
    dac_addresses = [dac["id"] for dac in CFG["dac"] if dac["found"]]
    offline_dacs = [dac for dac in CFG["dac"] if not dac["found"]]
    return render_template('config/index.html', online_dacs=online_dacs, offline_dacs=offline_dacs, dac_addresses=dac_addresses, dac_objects=dac_objects)

############################ Engine Starter ###################################

@app.route('/start-engine', methods=['POST'])
def start_engine():
    relay_controller = RelayController(address=0x27)
    try:
        if engine_state == True:
            relay_controller.off(1)
            print('Turning Engine off')
            engine_state = False
            return jsonify({'success': True, 'message': 'Live turned off'})
        else:
            relay_controller.enginestarter(live=1, starter=2)  # Assuming pin numbers are correct
            print('Attempting to start engine')
            engine_state = True
            return jsonify({'success': True, 'message': 'Engine started, live on'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    
############################ Config Functions ###################################
@app.route('/config', methods=['GET'])
def get_dac_config():
    existing_configs = load_config()
    serialized_cfg = {
        "dac": [
            {"name": item["name"], "id": item["id"], "found": item["found"],
                "current_voltage": item["current_voltage"]}
            for item in CFG["dac"]
        ]
    }
    return jsonify({'dac_addresses': serialized_cfg, 'existing_configs': existing_configs})


# Route to serve HTML form for updating configuration
@app.route('/update_config/<string:section>/<int:index>', methods=['GET'])
def update_config_form(section, index):
    return render_template('update_config.html', section=section, index=index)


# Route to update a specific configuration item
@app.route('/config/<string:section>/<int:index>', methods=['PUT'])
def update_config(section, index):
    data = load_config()
    new_value = request.json
    data[section][index] = new_value
    save_config(data)
    return jsonify(data[section][index])


@app.route('/config', methods=['PUT'])
@app.route('/config', methods=['PUT'])
def update_all_config():
    try:
        data = request.json
        settings = data.get('settings', [])
        preset_data = data.get('presets', {})

        config = load_config()

        # Update DAC configurations
        for setting in settings:
            for dac in config["dac"]:
                if dac["id"] == setting["id"]:
                    dac["name"] = setting.get("name", dac["name"])

        # Update presets
        if preset_data:
            config["presets"].update(preset_data)

        # Save the updated configurations
        save_config(config)

        return jsonify({"message": "Configurations updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



########################### Voltage Control ####################################

@app.route('/set_voltage<addr>', methods=['POST'])
def set_voltage(addr):
    voltage = float(request.form['voltage'])
    return set_voltage_action(addr, voltage)


@app.route('/close1<addr>', methods=['POST'])
def close1(addr):
    return set_voltage_action(addr, 0)


@app.route('/open1<addr>', methods=['POST'])
def open1(addr):
    return set_voltage_action(addr, 10000)


@app.route('/get_current_voltage/<string:dac_id>', methods=['GET'])
def get_current_voltage(dac_id):
    try:
        # Find the DAC object with the given ID
        dac = next((dac for dac in CFG["dac"] if dac["id"] == dac_id), None)
        if dac:
            # Return the current voltage of the DAC
            return jsonify({'voltage': dac.get('current_voltage', 0)})
        else:
            return jsonify({'error': 'DAC not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

########################### Preset Control ####################################


def add_preset(name, values):
    config = load_config()
    presets = config["existing_configs"]["presets"]
    if "presets" not in config:
        config["presets"] = {}
    config["presets"][name] = values  # values = {"addr": "0-100", etc.}
    save_config(config)


@app.route('/get_presets', methods=['GET'])
def get_presets():
    config = load_config()
    return config.get("presets", {})


@app.route('/delete_preset/<preset_name>', methods=['POST'])
def delete_preset(preset_name):
    config = load_config()
    if "presets" in config and preset_name in config["presets"]:
        del config["presets"][preset_name]
        save_config(config)
        return jsonify({'message': 'Preset deleted successfully'}), 200
    else:
        return jsonify({'error': 'Preset not found'}), 404


@app.route('/save_preset', methods=['POST'])
def save_preset():
    data = request.json
    if 'name' not in data or 'values' not in data:
        return jsonify({'error': 'Missing name or values'}), 400

    config = load_config()
    if "presets" not in config:
        config["presets"] = {}

    config["presets"][data['name']] = data['values']
    print("Preparing to save preset:",
          config["presets"][data['name']])  # Debug print

    save_config(config)
    return jsonify({'message': 'Preset saved successfully'}), 200


@app.route('/apply_preset', methods=['POST'])
def apply_preset():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'No preset name provided'}), 400

    flush_check(name)
    config = load_config()
    presets = config.get("presets", {})

    if name not in presets:
        print(f"Preset {name} not found.")
        return jsonify({'error': f'Preset {name} not found'}), 404

    preset_values = presets[name]
    for dac_addr, percentage in preset_values.items():
        result = set_voltage_action(dac_addr, percentage)
        print(result)

    return jsonify({'message': f'Preset {name} applied successfully'}), 200


def flush_check(preset_name):
    dac_addresses = [dac["id"] for dac in CFG["dac"] if dac["found"]]
    preset_addresses = CFG["presets"].get(preset_name, {}).keys()

    for addr in dac_addresses:
        if addr not in preset_addresses:
            for adr in dac_addresses:
                set_voltage_action(adr, 0)
            break
    time.sleep(preset_flush_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
