from flask import Blueprint, jsonify, request

from core.config import w_logger as logger
from database.db import db
from models.water import Water


water_bp = Blueprint('water', __name__)


# Get all water states
@water_bp.get('/waterstates')
def get_all_light_states():
    waters = Water.query.all()
    water_states = [water.to_dict() for water in waters]
    logger.info('Retrieved all water states')
    return jsonify(water_states), 200


# Get water system state
@water_bp.get('/waterstate/<int:water_id>')
def get_water_state(water_id):
    water = Water.query.get(water_id)
    if water:
        logger.info(f'Water system {water_id} state retrieved: {water.status}')
        return jsonify(water.to_dict()), 200
    else:
        logger.warning(f'Water system {water_id} not found')
        return jsonify({"error": "Water system not found"}), 404


# Update water system state
@water_bp.patch('/waterstates/<int:water_id>')
def update_water_state(water_id):
    water = Water.query.get(water_id)
    if not water:
        logger.warning(f'Attempt to update non-existing water system {water_id}')
        return jsonify({"error": "Water system not found"}), 404

    data = request.get_json()
    action = data.get('status')

    if action in ['on', 'off']:
        water.status = action
        db.session.commit()
        logger.info(f'Water system {water_id} turned {action}')
        return jsonify({"status": f"Water system {water_id} turned {action}"}), 200
    else:
        logger.error(f'Invalid action attempted on water system {water_id}: {action}')
        return jsonify({"error": "Invalid action"}), 400
