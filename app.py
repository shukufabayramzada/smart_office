from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models.models import Light, WaterSystem
from database.db import db
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click


app = Flask(__name__)
CORS(app, origins=["https://smartof.vercel.app"])


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_office.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@click.command(name='add_sample_data')
@with_appcontext
def add_sample_data():
    # Add sample lights
    if not Light.query.first():
        light1 = Light(id=1, status='on')
        light2 = Light(id=2, status='on')
        light3 = Light(id=3, status='on')
        db.session.add_all([light1, light2, light3])
        db.session.commit()

    # Add sample water systems
    if not WaterSystem.query.first():
        water1 = WaterSystem(id=1, status='on')
        water2 = WaterSystem(id=2, status='on')
        db.session.add_all([water1, water2])
        db.session.commit()

    print("Sample data added to the database.")

# Register the command with the Flask app
app.cli.add_command(add_sample_data)


# Routes
@app.route("/")
def index():
    return "Welcome to Smart Office!"

# Get light state
@app.route('/lightstate/<int:light_id>', methods=['GET'])
def get_light_state(light_id):
    light = Light.query.get(light_id)
    if light:
        return jsonify(light.to_dict()), 200
    else:
        return jsonify({"error": "Light not found"}), 404

# Update light state
@app.route('/light/<int:light_id>', methods=['PATCH'])
def update_light_state(light_id):
    light = Light.query.get(light_id)
    if not light:
        return jsonify({"error": "Light not found"}), 404

    data = request.get_json()
    action = data.get('action')

    if action in ['on', 'off']:
        light.status = action
        db.session.commit()
        return jsonify({"status": f"Light {light_id} turned {action}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400

# Get water system state
@app.route('/waterstate/<int:water_id>', methods=['GET'])
def get_water_state(water_id):
    water = WaterSystem.query.get(water_id)
    if water:
        return jsonify(water.to_dict()), 200
    else:
        return jsonify({"error": "Water system not found"}), 404

# Update water system state
@app.route('/water/<int:water_id>', methods=['PATCH'])
def update_water_state(water_id):
    water = WaterSystem.query.get(water_id)
    if not water:
        return jsonify({"error": "Water system not found"}), 404

    data = request.get_json()
    action = data.get('action')

    if action in ['on', 'off']:
        water.status = action
        db.session.commit()
        return jsonify({"status": f"Water system {water_id} turned {action}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
