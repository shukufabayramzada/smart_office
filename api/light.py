from flask import Blueprint, jsonify, request

from database.db import db
from models.light import Light


light_bp = Blueprint('light', __name__)


# Get all light states
@light_bp.get('/lightstates')
def get_all_light_states():
    lights = Light.query.all()
    light_states = [light.to_dict() for light in lights]
    return jsonify(light_states), 200


# Get light state
@light_bp.get('/lightstate/<int:light_id>')
def get_light_state(light_id):
    light = Light.query.get(light_id)
    if light:
        return jsonify(light.to_dict()), 200
    else:
        return jsonify({"error": "Light not found"}), 404


# Update light state
@light_bp.patch('/lightstates/<int:light_id>')
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
