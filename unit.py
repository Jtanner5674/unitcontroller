from flask import Flask, render_template, request, jsonify
import DFRobot_GP8403
import json
import traceback
import busio
import board

dac_objects = {}
dac_addresses = {}

app = Flask(__name__)

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

    dac_list = CFG.get("dac", [])

    for item in dac_list:
        if isinstance(item, dict):
            item["found"] = False

    try:
        i2c = busio.I2C(board.SCL, board.SDA)

        print("Scanning I2C bus for DACs...")
        index = 0
        for o in range(8, 16):
            addr = 0x50 + o
            try:
                dac = DFRobot_GP8403.DFRobot_GP8403(addr)
                dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
                dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL0)
                dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL1)
                for i, item in enumerate(dac_list):
                    if item["id"] == addr:
                        item["found"] = True
                        break
                else:
                    dac_list.append({"name": "", "id": addr, "found": True, "dac": dac})
                print(f"DAC found at address {hex(addr)}.")
                dac_addresses[index] = addr
                CFG["dac_addresses"]["dac"].append({hex(addr)})
                index += 1
            except Exception as e:
                print(f"No DAC found at address {hex(addr)}")
                continue

        # Additional cleanup logic if needed
        for i in dac_list:
            if i["found"] is False and i["name"] != "":
                print(f"Failed to find DAC {i['name']} at {i['id']}")
            else:
                dac_list.remove(i)

        # Update CFG to be a dictionary
        CFG = {"dac": dac_list}

        print(CFG)
        return CFG

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
    existing_configs = load_config()
    return jsonify({'dac_addresses': CFG, 'existing_configs': existing_configs})

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
        
        # Update the in-memory representation (CFG["dac"])
        for setting in filtered_settings:
            for dac in CFG["dac"]:
                if dac["id"] == setting["id"]:
                    dac["chan"] = setting["chan"]
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