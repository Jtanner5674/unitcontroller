import json
from flask import Flask, render_template, jsonify, request

@app.route('/settings/')
def index():
    return render_template('index.html')

# Function to load JSON data from a file
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Function to save JSON data to a file
def save_config(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=2)

# Route to serve HTML form for updating configuration
@app.route('/update_config/<string:section>/<int:index>', methods=['GET'])
def update_config_form(section, index):
    return render_template('update_config.html', section=section, index=index)

# Route to get the entire configuration
@app.route('/config', methods=['GET'])
def get_config():
    data = load_config()
    return jsonify(data)

# Route to update a specific configuration item
@app.route('/config/<string:section>/<int:index>', methods=['PUT'])
def update_config(section, index):
    data = load_config()
    new_value = request.json  # New value from the request
    data[section][index] = new_value  # Update the specified item
    save_config(data)  # Save updated data to the file
    return jsonify(data[section][index])