from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403

app = Flask(__name__)

dac_objects = {}
dac_addresses = {}

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

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', dac_objects=dac_objects)

def set_voltage_action(dac_id, channel):
    addr = dac_addresses.get(dac_id)
    dac = DFRobot_GP8403.DFRobot_GP8403(addr)
    if dac:
        percentage = float(request.form[f'voltage{channel}'])
        voltage = 2 + (percentage / 100) * 8
        volts = voltage * 500
        channel_num = DFRobot_GP8403.CHANNEL0 if channel == 1 else DFRobot_GP8403.CHANNEL1
        dac.set_DAC_out_voltage(volts, channel_num)
        errval = f'Voltage set to {voltage}V for Channel {channel_num} on address {hex(addr)} with id {dac_id}'
        return jsonify({'message': errval})  # Return a JSON response for AJAX handling
    else:
        return jsonify({'error': 'Invalid DAC ID'})

@app.route('/set_voltage<int:dac_id>', methods=['POST'])
def set_voltage1(dac_id):
    return set_voltage_action(dac_id, 1)

@app.route('/set_voltage2<int:dac_id>', methods=['POST'])
def set_voltage2(dac_id):
    return set_voltage_action(dac_id, 2)

def channel_action(dac_id, channel, value):
    dac = dac_objects.get(dac_id)
    if dac:
        voltage = 10000 if value == 'open' else 2000
        channel_num = DFRobot_GP8403.CHANNEL0 if channel == 1 else DFRobot_GP8403.CHANNEL1
        dac.set_DAC_out_voltage(voltage, channel_num)
        return jsonify({'message': f'{value.capitalize()}ed Channel {channel_num} on DAC {dac_id}'})
    else:
        return jsonify({'error': 'Invalid DAC ID'})


@app.route('/close1<int:dac_id>')
def close1(dac_id):
    return channel_action(dac_id, 1, 'open')

@app.route('/close2<int:dac_id>')
def close2(dac_id):
    return jsonify({'message': channel_action(dac_id, 2, 'close')})

@app.route('/open1<int:dac_id>')
def open1(dac_id):
    return jsonify({'message': channel_action(dac_id, 1, 'open')})

@app.route('/open2<int:dac_id>')
def open2(dac_id):
    return jsonify({'message': channel_action(dac_id, 2, 'open')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)