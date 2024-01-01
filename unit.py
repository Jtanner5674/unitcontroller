from flask import Flask, render_template, request, jsonify
from DFRobot_GP8403 import DFRobot_GP8403

app = Flask(__name__)

# Initialize your DAC object
dac = DFRobot_GP8403(0x58)  # Replace 0x58 with your DAC's address

# Start with both Closed
dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)  # Set 2V on channel 1
dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)  # Set 2V on channel 2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_current_voltages', methods=['GET'])
def get_current_voltages():
    voltage1 = dac.read_DAC_out_voltage(DFRobot_GP8403.CHANNEL0)
    voltage2 = dac.read_DAC_out_voltage(DFRobot_GP8403.CHANNEL1)
    return jsonify({'voltage1': voltage1, 'voltage2': voltage2})

@app.route('/set_voltage1', methods=['POST'])
def set_voltage1():
    percentage = float(request.form['voltage1'])
    voltage = 2 + (percentage / 100) * 8  # Convert percentage to the 2-10 range
    dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL0)  # Set voltage on channel 1
    return f'Voltage set to {voltage}V for Channel 1'

@app.route('/set_voltage2', methods=['POST'])
def set_voltage2():
    percentage = float(request.form['voltage2'])
    voltage = 2 + (percentage / 100) * 8  # Convert percentage to the 2-10 range
    dac.set_DAC_out_voltage(voltage, DFRobot_GP8403.CHANNEL1)  # Set voltage on channel 2
    return f'Voltage set to {voltage}V for Channel 2'

@app.route('/closed1')
def set_closed1():
    dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL0)  # Set 2V on channel 1
    return 'Closed'

@app.route('/open1')
def set_open1():
    dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL0)  # Set 10V on channel 1
    return 'Open'

@app.route('/closed2')
def set_closed2():
    dac.set_DAC_out_voltage(2, DFRobot_GP8403.CHANNEL1)  # Set 2V on channel 2
    return 'Closed'

@app.route('/open2')
def set_open2():
    dac.set_DAC_out_voltage(10, DFRobot_GP8403.CHANNEL1)  # Set 10V on channel 2
    return 'Open'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
