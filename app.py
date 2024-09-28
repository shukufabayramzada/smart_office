from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# State variables to track the status of light and water
light_state = {"status": "off"}
water_state = {"status": "off"}

# ESP32 IP address (replace with actual IP of ESP32)
ESP32_IP = "http://<your_esp32_ip>"

# Light Control: Turn on/off light
@app.route('/lightstate', methods=['POST'])
def control_light():
    data = request.json
    action = data.get('action')

    if action == "on":
        light_state['status'] = "on"
        # Send request to ESP32 to turn the light ON
        try:
            requests.post(f"{ESP32_IP}/light/on")
            return jsonify({"status": "Light turned on"}), 200
        except:
            return jsonify({"error": "Failed to reach ESP32"}), 500
    elif action == "off":
        light_state['status'] = "off"
        # Send request to ESP32 to turn the light OFF
        try:
            requests.post(f"{ESP32_IP}/light/off")
            return jsonify({"status": "Light turned off"}), 200
        except:
            return jsonify({"error": "Failed to reach ESP32"}), 500
    else:
        return jsonify({"error": "Invalid action"}), 400

# Get Light State: Check the status of the light
@app.route('/lightstate', methods=['GET'])
def get_light_state():
    return jsonify(light_state)

# Water Control: Turn on/off water system
@app.route('/waterstate', methods=['POST'])
def control_water():
    data = request.json
    action = data.get('action')

    if action == "on":
        water_state['status'] = "on"
        # Send request to ESP32 to turn the water ON
        try:
            requests.post(f"{ESP32_IP}/water/on")
            return jsonify({"status": "Water turned on"}), 200
        except:
            return jsonify({"error": "Failed to reach ESP32"}), 500
    elif action == "off":
        water_state['status'] = "off"
        # Send request to ESP32 to turn the water OFF
        try:
            requests.post(f"{ESP32_IP}/water/off")
            return jsonify({"status": "Water turned off"}), 200
        except:
            return jsonify({"error": "Failed to reach ESP32"}), 500
    else:
        return jsonify({"error": "Invalid action"}), 400

# Get Water State: Check the status of the water system
@app.route('/waterstate', methods=['GET'])
def get_water_state():
    return jsonify(water_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
