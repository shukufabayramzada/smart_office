from flask import Blueprint, jsonify, request

from core.config import l_logger as logger
from database.db import db
from models.light import Light


light_bp = Blueprint('light', __name__)


# Get all light states
@light_bp.get('/lightstates')
def get_all_light_states():
    lights = Light.query.all()
    light_states = [light.to_dict() for light in lights]
    logger.info('Retrieved all light states')
    return jsonify(light_states), 200


# Get light state
@light_bp.get('/lightstate/<int:light_id>')
def get_light_state(light_id):
    light = Light.query.get(light_id)
    if light:
        logger.info(f'Light {light_id} state retrieved: {light.status}')
        return jsonify(light.to_dict()), 200
    else:
        logger.warning(f'Light {light_id} not found')
        return jsonify({"error": "Light not found"}), 404


# Update light state
@light_bp.patch('/lightstates/<int:light_id>')
def update_light_state(light_id):
    light = Light.query.get(light_id)
    if not light:
        logger.warning(f'Attempt to update non-existing light {light_id}')
        return jsonify({"error": "Light not found"}), 404

    data = request.get_json()
    action = data.get('status')

    if action in ['on', 'off']:
        light.status = action
        db.session.commit()
        logger.info(f'Light {light_id} turned {action}')
        return jsonify({"status": f"Light {light_id} turned {action}"}), 200
    else:
        logger.error(f'Invalid action attempted on light {light_id}: {action}')
        return jsonify({"error": "Invalid action"}), 400
