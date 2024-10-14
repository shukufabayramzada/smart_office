from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# State variables to track the status of light and water
light_state = {"status": "on"}
water_state = {"status": "off"}


# Get Light State: Check the status of the light
@app.route('/lightstate', methods=['GET'])
def get_light_state():
    return jsonify(light_state)

# Get Water State: Check the status of the water system
@app.route('/waterstate', methods=['GET'])
def get_water_state():
    return jsonify(water_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
