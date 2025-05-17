from flask import Blueprint, request, jsonify, current_app
from algorithms.placement import hybrid_guillotine_cut_genetic_algorithm
import uuid
from datetime import datetime

placement_bp = Blueprint('placement', __name__)


@placement_bp.route('/placement', methods=['POST'])
def placement():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    items = data.get('items', [])
    containers = data.get('containers', [])

    # Verify required data
    if not items or not containers:
        return jsonify({"success": False, "error": "Items and containers are required"}), 400

    # Generate placements and rearrangements
    placements, rearrangements = hybrid_guillotine_cut_genetic_algorithm(items, containers)

    # Store the result in our in-memory database
    current_app.config['CONTAINERS'] = containers

    for placement in placements:
        item_id = placement["itemId"]
        item = next((item for item in items if item["itemId"] == item_id), None)

        if item:
            item["containerId"] = placement["containerId"]
            item["position"] = placement["position"]

    current_app.config['ITEMS'] = items

    # Log the placement operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "placement",
        "details": {
            "numItems": len(items),
            "numContainers": len(containers)
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "placements": placements,
        "rearrangements": rearrangements
    })
