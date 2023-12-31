// Load existing configuration if available
// Fetch existing config on page load
fetch('/getConfig')
    .then(response => response.json())
    .then(config => {
        // Handle the received config data, populate the settings on the page
    })
    .catch(error => console.error('Error:', error));

// Function to generate settings for each device type
function generateSettings(type, devices) {
    const container = document.getElementById(`${type.toLowerCase()}Settings`);
    container.innerHTML = '';

    devices.forEach((device, index) => {
        const div = document.createElement('div');
        div.innerHTML = `
            <label for="${type}_${index}_addr">Address:</label>
            <input type="text" id="${type}_${index}_addr" value="${device.ADDR}" disabled>

            <label for="${type}_${index}_name">Name:</label>
            <input type="text" id="${type}_${index}_name" value="${device.NAME}">

            ${type === 'DAC' ? `
                <label for="${type}_${index}_channel">Channel:</label>
                <select id="${type}_${index}_channel">
                    <option value="0" ${device.CHANNEL === '0' ? 'selected' : ''}>0</option>
                    <option value="1" ${device.CHANNEL === '1' ? 'selected' : ''}>1</option>
                </select>
            ` : ''}
            <br><br>
        `;
        container.appendChild(div);
    });
}

// Function to save settings to config.json

function saveConfig(updatedConfig) {
    fetch('/saveConfig', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedConfig)
    })
    .then(response => {
        if (response.ok) {
            console.log('Config updated successfully!');
        } else {
            console.error('Config update failed.');
        }
    })
    .catch(error => console.error('Error:', error));
}
    // Save the config object to config.json
    // Replace this with code to write the updated config object to the config.json file
}
