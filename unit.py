from flask import Flask, render_template, request, jsonify
import DFRobot_GP8403
import json
import traceback
import busio
import board
from flask_cors import CORS

dac_objects = {}
dac_addresses = {}

app = Flask(__name__)
CORS(app)

CFG = None  # Initialize CFG as None


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)


def initialize_dacs():
    global CFG
    CFG = load_config()
    global dac_objects
    dac_objects = {}
    dac_list = CFG.get("dac", [])

    for item in dac_list:
        if isinstance(item, dict):
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

                found_dac = next((item for item in dac_list if item["id"] == hex(addr)), None)
                if found_dac:
                    found_dac["found"] = True
                    found_dac["obj"] = dac
                    dac_objects[found_dac["id"]] = found_dac
                else:
                    new_dac = {"name": "", "id": hex(addr), "found": True, "obj": dac, "current_voltage": 0}
                    existing_config = next(
                        (config for config in CFG["existing_configs"]["dac"] if config["id"] == new_dac["id"]),
                        None)
                    if existing_config:
                        new_dac.update(existing_config)
                    dac_list.append(new_dac)
                    dac_objects[new_dac["id"]] = new_dac

                print(f"DAC found at address {hex(addr)}.")
            except Exception as e:
                print(f"No DAC found at address {hex(addr)}")
                continue

        # Additional cleanup logic if needed
        dac_list = [item for item in dac_list if item["found"]]

        # Update CFG to be a dictionary
        CFG = {"dac": dac_list}

        print(CFG)
        return CFG

    except Exception as e:
        print("Error while scanning for DACs:", e)

def add_preset(name, values):
    config = load_config()
    if "presets" not in config:
        config["presets"] = {}
    config["presets"][name] = values
    save_config(config)

def delete_preset(name):
    config = load_config()
    if "presets" in config and name in config["presets"]:
        del config["presets"][name]
        save_config(config)

@app.route('/get_presets', methods=['POST'])
def get_presets():
    config = load_config()
    return config.get("presets", {})

def apply_preset(name):
    config = load_config()
    presets = config.get("presets", {})
    if name not in presets:
        print(f"Preset {name} not found.")
        return
    preset_values = presets[name]
    for dac_addr, percentage in preset_values.items():
        voltage = int((float(percentage) / 100.0) * 10000)
        result = set_voltage_action(dac_addr, voltage)
        print(result)


@app.route('/save_preset', methods=['POST'])
def save_preset():
    data = request.json  # Preset data from the request
    config = load_config()  # Load current config
    if "presets" not in config:
        config["presets"] = []
    config["presets"].append(data)  # Append the new preset
    save_config(config)  # Save the updated config back to file
    return jsonify({'message': 'Preset saved successfully'}), 200

@app.route('/edit_preset/<preset_name>', methods=['POST'])
def edit_preset(preset_name):
    config = load_config()
    preset_data = request.json
    if "presets" in config and preset_name in config["presets"]:
        config["presets"][preset_name] = preset_data
        save_config(config)
        return jsonify({'message': 'Preset edited successfully'}), 200
    else:
        return jsonify({'error': 'Preset not found'}), 404

@app.route('/delete_preset/<preset_name>', methods=['POST'])
def delete_preset(preset_name):
    config = load_config()
    if "presets" in config and preset_name in config["presets"]:
        del config["presets"][preset_name]
        save_config(config)
        return jsonify({'message': 'Preset deleted successfully'}), 200
    else:
        return jsonify({'error': 'Preset not found'}), 404


# Initialize DACs when the script starts
CFG = initialize_dacs()



# Flask Routes
print(dac_addresses)
@app.route('/')
def index():
    existing_configs = load_config()
    return render_template('index.html', dac_objects=dac_objects, dac_addresses=dac_addresses, existing_configs=existing_configs)



@app.route('/settings')
def settings():
    return render_template('config/index.html')


def set_voltage_action(addr, value):
    try:
        
        addr_int = int(addr, 16)  # Convert hex string to integer for comparison
        dac = next(d for d in CFG["dac"] if int(d["id"], 16) == addr_int)
        dac["obj"].set_DAC_out_voltage(value, DFRobot_GP8403.CHANNEL0)
        dac["obj"].set_DAC_out_voltage(value, DFRobot_GP8403.CHANNEL1)
        volts = float(value / 1000)
        dac["current_voltage"] = value 
        print(f'{dac["name"]} set to {volts}V')
        return jsonify({'message': f'{dac["name"]} set to {volts}V'})
    except StopIteration:
        print('error: Invalid DAC ADDR')
        return jsonify({'error': 'Invalid DAC ADDR'})

@app.route('/set_voltage<addr>', methods=['POST'])
def set_voltage(addr):
    voltage = float(request.form['voltage'])
    voltage = int((voltage / 100.0) * 10000)
    return set_voltage_action(addr, voltage)


@app.route('/close1<addr>', methods=['POST'])
def close1(addr):
    return set_voltage_action(addr, 0)


@app.route('/open1<addr>', methods=['POST'])
def open1(addr):
    return set_voltage_action(addr, 10000)


@app.route('/config', methods=['GET'])
def get_dac_config():
    existing_configs = load_config()

    # Manually serialize CFG, excluding DFRobot_GP8403 objects
    serialized_cfg = {
        "dac": [
            {"name": item["name"], "id": item["id"],"found": item["found"], "current_voltage": item["current_voltage"]}
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
    new_value = request.json  # New value from the request
    data[section][index] = new_value  # Update the specified item
    save_config(data)  # Save updated data to the file
    return jsonify(data[section][index])

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

@app.route('/config', methods=['PUT'])
def update_all_config():
    try:
        data = request.json  # New values from the request
        filtered_settings = [setting for setting in data['settings'] if setting['id'] != 'offline']
        print("Received data:", filtered_settings)  # Add this line for debugging

        # Update the in-memory representation (CFG["dac"])
        for setting in filtered_settings:
            for dac in CFG["dac"]:
                if dac["id"] == setting["id"]:
                    dac["name"] = setting["name"]

        # Update the top part of the JSON file
        CFG["dac_addresses"] = CFG["dac"]

        # Save updated data to the file
        save_config(filtered_settings)

        return jsonify({"message": "Configurations updated successfully"})
    except Exception as e:
        traceback.print_exc()  # Print the traceback for detailed error information
        return jsonify({"error": str(e)}), 500  # Return an error message and status code 500 for an internal server error


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)