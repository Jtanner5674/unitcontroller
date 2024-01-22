from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403
import json

app = Flask(__name__)

dac_objects = {}
dac_addresses = {}

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config():
    T_CFG = CFG.copy()
    for value in T_CFG["dac"]:
        value.pop('dac', None)  # this will not crash if the element has no key 'dac'
    with open('config.json', 'w') as file:
        json.dump(T_CFG, file, indent=2)


CFG=load_config()

for item in CFG["dac"]:
    item["found"] = False

print(CFG)

print("Scanning I2C bus for DACs...")
for o in range(8, 16):  # Equivalent to the range 8..F in hexadecimal
    addr = 0x50 + o
    try:
        dac = DFRobot_GP8403.DFRobot_GP8403(addr)
        dac.set_DAC_outrange(DFRobot_GP8403.OUTPUT_RANGE_10V)
        dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL0)
        dac.set_DAC_out_voltage(2000, DFRobot_GP8403.CHANNEL1)
        for i, item in enumerate(CFG["dac"]):
            if item["id"] == addr:
                # existing
                item["found"] = True
                item["obj"] = dac
                break
        else:
            # new
            CFG["dac"].append({"name": "", "id": addr, "found": True, "dac": dac})
    except Exception as e:
        print(f"No DAC found at address {hex(addr)}")
        continue
print(CFG)
for i in CFG["dac"]:
    if i["found"] == False and i["name"]!="":
        print(f"Failed to find dac {i['name']} at {i['id']}")
      # Indicate in UI that a named DAC is missing
    else:
      # remove missing unnamed
      CFG["dac"].remove(i)
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

# Route to get the entire configuration
@app.route('/config', methods=['GET'])
def get_dac_config():
    existing_configs = load_config()
    return jsonify({'dac_addresses': CFG["dac"], 'existing_configs': existing_configs})

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
        save_config(data['settings'])  # Save updated data to the file
        return jsonify({"message": "All configurations updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error message and status code 500 for internal server error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    