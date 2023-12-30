from flask import Flask, render_template, request, jsonify
import busio
import board
import DFRobot_GP8403

app = Flask(__name__)

dac_objects = {}  # Dictionary to store DACS with IDs

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
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
            dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
            dac_objects[index] = dac  # Store DAC object with ID
            print(f"DAC found at address {hex(addr)} with ID {index}.")
            index += 1
        except Exception as e:
            print(f"No DAC found at address {hex(addr)}")
            continue

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html', dac_objects=dac_objects)


@app.route('/set_voltage<int:dac_id>', methods=['POST'])
def set_voltage(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        percentage = float(request.form['voltage1'])
        voltage = 2 + (percentage / 100) * 8
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)
        return f'Voltage set to {voltage}V for Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/set_voltage2<int:dac_id>', methods=['POST'])
def set_voltage2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        percentage = float(request.form['voltage2'])
        voltage = 2 + (percentage / 100) * 8
        dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL1)
        return f'Voltage set to {voltage}V for Channel 2 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/close1<int:dac_id>')
def close1(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)
        return f'Closed Channel 0 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/close2<int:dac_id>')
def close2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)
        return f'Closed Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/open1<int:dac_id>')
def open1(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL0)
        return f'Opened Channel 0 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

@app.route('/open2<int:dac_id>')
def open2(dac_id):
    dac = dac_objects.get(dac_id)
    if dac:
        dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL1)
        return f'Opened Channel 1 on DAC {dac_id}'
    else:
        return 'Invalid DAC ID'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)