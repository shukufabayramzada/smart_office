from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/swagger'  
API_URL = '/static/swagger.json'  

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

light_state = {"status": "on"}
water_state = {"status": "on"}

@app.route('/lightstate', methods=['GET'])
def get_light_state():
    return jsonify(light_state)

@app.route('/light/on', methods=['POST'])
def turn_on_light():
    light_state["status"] = "on"
    return jsonify({"status": "Light turned on"}), 200

@app.route('/light/off', methods=['POST'])
def turn_off_light():
    light_state["status"] = "off"
    return jsonify({"status": "Light turned off"}), 200

@app.route('/waterstate', methods=['GET'])
def get_water_state():
    return jsonify(water_state)

@app.route('/water/on', methods=['POST'])
def turn_on_water():
    water_state["status"] = "on"
    return jsonify({"status": "Water system turned on"}), 200

@app.route('/water/off', methods=['POST'])
def turn_off_water():
    water_state["status"] = "off"
    return jsonify({"status": "Water system turned off"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    