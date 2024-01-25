from flask import Flask, render_template, request, jsonify
import DFRobot_GP8403
import json
import traceback
import busio
import board
from json import JSONEncoder

dac_objects = {}

app = Flask(__name__)

class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DFRobot_GP8403):
            return obj.__dict__  # Serialize class attributes
        return super().default(obj)

CFG = None  # Initialize CFG as None

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config(settings):
    with open('config.json', 'w') as file:
        json.dump({"dac": settings}, file, indent=2)


def initialize_dacs():
    global CFG  # Use the global CFG variable
    CFG = load_config()

    if isinstance(CFG, list):
        # If CFG is a list, assume it's the "dac" section of the configuration
        CFG = {"dac": CFG}

    dac_list = CFG.get("dac", [])

    for item in dac_list:
        if isinstance(item, dict):
            item["found"] = False

    try:
        i2c = busio.I2C(board.SCL, board.SDA)

        print("Scanning I2C bus for DACs...")
        for o in range(8, 16):  # Equivalent to the range 8..F in hexadecimal
            addr = 0x50 + o
            try:
                dac = DFRobot_GP8403.DFRobot_GP8403(addr)
                dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
                dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL0)
                dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL1)
                for i, item in enumerate(dac_list):
                    if item["id"] == addr:
                        # existing
                        item["found"] = True
                        item["dac"] = dac
                        break
                else:
                    # new
                    dac_list.append({"name": "", "id": addr, "found": True, "dac": dac})
                print(f"DAC found at address {hex(addr)}.")
            except Exception as e:
                print(f"No DAC found at address {hex(addr)}")
                continue

        dac_list = [i for i in dac_list if i["found"] or i["name"] == ""]


        # Update CFG["dac"]
        CFG["dac"] = dac_list

        print(CFG)
        return CFG  # Return the modified CFG

    except Exception as e:
        print("Error while scanning for DACs:", e)

# Initialize DACs when the script starts
CFG = initialize_dacs()

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', dac_objects=dac_objects)

@app.route('/settings')
def settings():
    return render_template('config/index.html')


def set_voltage_action(addr, value):
    try:
        addr_int = int(addr, 16)     # Convert hex string to integer for comparison
        dac = next(d for d in CFG["dac"] if int(d["id"], 16) == addr_int)
        dac["obj"].set_DAC_out_voltage(value, DFRobot_GP8403.CHANNEL0 if dac["chan"] == 0 else DFRobot_GP8403.CHANNEL1)
        return jsonify({'message': f'{dac["name"]} set to {value}V'})
    except StopIteration:
        return jsonify({'error': 'Invalid DAC ADDR'})


@app.route('/set_voltage<int:addr>', methods=['POST'])
def set_voltage(addr):
    voltage = float(request.form['voltage'])
    return set_voltage_action(addr, voltage)
 # change to addr, in your dropdown list you can specify: name="NAME" value="ADDR"

@app.route('/close<int:addr>', methods=['POST'])
def close1(addr):
    return set_voltage_action(addr, 2000)

@app.route('/open<int:addr>', methods=['POST'])
def open1(addr):
    return set_voltage_action(addr, 10000)

@app.route('/config', methods=['GET'])
def get_dac_config():
    dac_addresses_serializable = CFG["dac_addresses"]

    existing_dac_configs = CFG["existing_configs"].get("dac", [])

    return jsonify({'dac_addresses': dac_addresses_serializable, 'existing_configs': existing_dac_configs}, cls=CustomEncoder)

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

@app.route('/config', methods=['PUT'])
def update_all_config():
    try:
        data = request.json  # New values from the request
        filtered_settings = [setting for setting in data['settings'] if setting['id'] != 'offline']
        print("Received data:", filtered_settings)  # Add this line for debugging

        existing_configs = load_config()

        # Update the in-memory representation (CFG["dac"])
        for setting in filtered_settings:
            for dac in CFG["dac"]:
                if dac["id"] == setting["id"]:
                    dac["chan"] = setting["chan"]
                    dac["name"] = setting["name"]

        # Preserve the existing non-"dac" configurations
        existing_configs["dac"] = CFG["dac"]

        # Save the entire existing_configs dictionary back to the file
        save_config(existing_configs)

        return jsonify({"message": "Configurations updated successfully", 'dac_addresses': CFG["dac"]})
    except Exception as e:
        traceback.print_exc()  # Print the traceback for detailed error information
        return jsonify({"error": str(e)}), 500  # Return an error message and status code 500 for an internal server error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)