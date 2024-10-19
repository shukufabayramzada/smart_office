from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models.light import Light
from models.water import Water
from database.db import db
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click


app = Flask(__name__)
CORS(app)


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
    if not Water.query.first():
        water1 = Water(id=1, status='on')
        water2 = Water(id=2, status='on')
        db.session.add_all([water1, water2])
        db.session.commit()

    print("Sample data added to the database.")


# Register the command with the Flask app
app.cli.add_command(add_sample_data)


# Routes
@app.route("/")
def index():
    return "Welcome to Smart Office!"


# Get all light states
@app.get('/lightstates')
def get_all_light_states():
    lights = Light.query.all()
    light_states = [light.to_dict() for light in lights]
    return jsonify(light_states), 200


# Get light state
@app.get('/lightstate/<int:light_id>')
def get_light_state(light_id):
    light = Light.query.get(light_id)
    if light:
        return jsonify(light.to_dict()), 200
    else:
        return jsonify({"error": "Light not found"}), 404


# Update light state
@app.patch('/lightstates/<int:light_id>')
def update_light_state(light_id):
    light = Light.query.get(light_id)
    if not light:
        return jsonify({"error": "Light not found"}), 404

    data = request.get_json()
    action = data.get('status')

    if action in ['on', 'off']:
        light.status = action
        db.session.commit()
        return jsonify({"status": f"Light {light_id} turned {action}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400


# Get all water states
@app.get('/waterstates')
def get_all_light_states():
    waters = Water.query.all()
    water_states = [water.to_dict() for water in waters]
    return jsonify(water_states), 200


# Get water system state
@app.get('/waterstate/<int:water_id>')
def get_water_state(water_id):
    water = Water.query.get(water_id)
    if water:
        return jsonify(water.to_dict()), 200
    else:
        return jsonify({"error": "Water system not found"}), 404


# Update water system state
@app.patch('/waterstates/<int:water_id>')
def update_water_state(water_id):
    water = Water.query.get(water_id)
    if not water:
        return jsonify({"error": "Water system not found"}), 404

    data = request.get_json()
    action = data.get('status')

    if action in ['on', 'off']:
        water.status = action
        db.session.commit()
        return jsonify({"status": f"Water system {water_id} turned {action}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
