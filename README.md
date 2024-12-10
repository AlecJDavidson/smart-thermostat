# Smart Thermostat

This project is a smart thermostat built using an ESP32. It allows users to control and read the temperature via a web interface and integrates seamlessly with Home Assistant for enhanced automation.

## Features

- **Temperature Control**: Set heating or cooling based on your preferences.
- **Web Interface**: Control the thermostat and view the current temperature from a browser.
- **Home Assistant Integration**: Automations and dashboard cards for centralized control.
- **WiFi Configuration**: Easily configure your WiFi settings.

## Getting Started

### Prerequisites

1. **Hardware Requirements**:

   - **ESP32**
   - **DHT11** sensor on GPIO pin **32** (Temperature reading)
   - **Relay 1** for heating control on GPIO pin **33**
   - **Relay 2** for cooling control on GPIO pin **25**
   - **Relay 3** for fan control on GPIO pin **26**

2. **Home Assistant**: To enable advanced automation and dashboard features.

3. **Software Requirements**:
   - Python or MicroPython installed on the ESP32.
   - A local network with WiFi.

---

## Installation

### ESP32 Setup

1. **Configure WiFi**:

   - Locate the `wifi_config_base.json` file in the `src` folder.
   - Populate it with your WiFi credentials:
     ```json
     {
       "ssid": "your_wifi_ssid",
       "password": "your_wifi_password"
     }
     ```
   - Rename this file to `wifi_config.json`.

2. **Update IP Addresses**:

   - Replace all instances of `<your-ip>` in the project with the actual IP address of your ESP32.

3. **Upload Files**:

   - Use a tool like `ampy` or an IDE like Thonny to upload the following files from the `src` folder to your ESP32:
     - `main.py`
     - `boot.py`
     - `relay.py`
     - `server.py`
     - `wifi.py`
     - `wifi_config.json`
     - `local_dht.py`

4. **Connect Hardware**:
   - DHT11 sensor: GPIO **32**
   - Heating relay: GPIO **33**
   - Cooling relay: GPIO **25**
   - Fan relay: GPIO **26**

---

### Home Assistant Integration

1. **Copy Configuration Files**:

   - Navigate to the `home_assistant_config` folder.
   - Copy the following YAML files to your Home Assistant configuration directory:
     - `rest_commands.yaml`
     - `dashboard_card.yaml`
     - `configuration.yaml`
     - `automations.yaml`

2. **Restart Home Assistant**:
   - After copying, restart your Home Assistant instance to apply the changes.

---

## REST API

The thermostat server hosts a REST API for controlling and monitoring the device. Use the IP address of your ESP32 to interact with the following endpoints:

### Endpoints

## Needs updated! Please view the endpoints in /<board>/src/api.py

1. **GET /api/temp**

   - **Description**: Retrieves the current temperature from the DHT11 sensor.
   - **Response**:
     ```json
     {
       "temperature_f": 72.5,
       "temperature_c": 22.5
     }
     ```

2. **POST /api/set_temperature**

   - **Description**: Sets the desired temperature for the thermostat.
   - **Body**:
     ```json
     {
       "set_temperature": 72
     }
     ```

3. **POST /api/mode**

   - **Description**: Changes the operating mode of the thermostat.
   - **Body**:
     ```json
     {
       "mode": "heat" // Options: "heat", "cool", "off"
     }
     ```

4. **GET /api/status**
   - **Description**: Returns the current status of the thermostat, including the set temperature, current temperature, and mode.
   - **Response**:
     ```json
     {
       "mode": "heat",
       "set_temperature": 72,
       "current_temperature_f": 72.5,
       "current_temperature_c": 22.5
     }
     ```

### Using the API

You can interact with these endpoints using tools like `curl`, Postman, or any HTTP client in your preferred programming language.

#### Example Requests

## Needs updated! Please view the endpoints in /<board>/src/api.py

#### GPIO Pins

## These can be set in /<board>/src/settings.py

| GPIO Pin | Function           | Connection |
| -------- | ------------------ | ---------- |
| **32**   | Temperature Sensor | DHT11      |
| **33**   | Heating Control    | Relay 1    |
| **25**   | Cooling Control    | Relay 2    |
| **26**   | Fan Control        | Relay 3    |

---

## License

This project is licensed under the terms specified in the `LICENSE` file.

## Contribution

Feel free to open issues or submit pull requests to improve the project!
