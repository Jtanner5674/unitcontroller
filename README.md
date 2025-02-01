UnitController - Web-Based Control for Pressure Washing Valves
Overview
UnitController is a Flask-based web server designed to control pressure washing valves via Digital-to-Analog Converters (DACs) on a Raspberry Pi. The system enables remote control of valves and relays through a web-based interface, making use of I2C communication and relay modules.
Features
Web-Based Control: Provides a web interface to manage valves and relays.
DAC Voltage Control: Adjusts valve states by setting DAC output voltages.
Engine Starter Control: Controls relays to start or stop the engine.
Preset Management: Allows users to save and apply voltage configurations.
I2C Device Detection: Automatically detects connected DACs on the I2C bus.
Hardware Setup
Power Distribution
12V Power Source: Feeds an amped distributor.
12V Valves: Directly powered from the distributor.
5V Step-Down Regulator: Powers DACs, relays, and the Raspberry Pi.
I2C Rail: Handles communication between the Raspberry Pi and DACs.
Software Setup
Prerequisites
Raspberry Pi Setup
Install Raspberry Pi OS (preferably Lite for headless operation).
Ensure Python 3 and Flask are installed.
Network Configuration
The Raspberry Pi must run an Access Point (AP) on boot to enable local network access.
I2C Configuration
Enable I2C on the Raspberry Pi using raspi-config.
Install required libraries for I2C communication.
Installation Steps
Clone the Repository
git clone https://github.com/Jtanner5674/unitcontroller.git
cd unitcontroller
Install Dependencies
pip install flask flask-cors busio board
Enable AP Mod
Follow Raspberry Pi AP setup guides.
Run UnitController on Boot
Add unit.py to system startup by modifying rc.local or creating a systemd service.
sudo nano /etc/rc.local
Add before exit 0:
python3 /path/to/unit.py &
Running the Application Manually
python3 unit.py
API Endpoints
Web Pages
/ - Main control interface
/settings - Configuration page
API Functions
Voltage Control
POST /set_voltage<addr> - Sets DAC voltage
POST /close1<addr> - Closes valve (0V)
POST /open1<addr> - Opens valve (100% voltage)
GET /get_current_voltage/<string:dac_id> - Retrieves current DAC voltage
Engine Control
POST /start-engine - Starts or stops the engine
Preset Management
GET /get_presets - Retrieves stored presets
POST /save_preset - Saves a new preset
POST /apply_preset - Applies a stored preset
POST /delete_preset/<preset_name> - Deletes a preset
Troubleshooting
I2C Devices Not Detected: Ensure correct wiring and I2C is enabled in raspi-config.
DAC Output Incorrect: Check power supply and DAC address configuration.
