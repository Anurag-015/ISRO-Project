from flask import Blueprint, request, jsonify, current_app
from algorithms.search import bm25_spatial_filtering_search
from algorithms.retrieval import retrieval_algorithm_3d_a_star_rtree
import uuid
from datetime import datetime

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET'])
def search():
    item_id = request.args.get('itemId')
    item_name = request.args.get('itemName')
    user_id = request.args.get('userId', 'anonymous')

    items = current_app.config.get('ITEMS', [])
    current_date = current_app.config.get('CURRENT_DATE', '2025-04-06')

    # Must provide either itemId or itemName
    if not item_id and not item_name:
        return jsonify({"success": False, "error": "Item ID or name is required"}), 400

    # Search by ID or name
    if item_id:
        found_item = next((item for item in items if item.get("itemId") == item_id), None)
    else:
        search_results = bm25_spatial_filtering_search(item_name, items, current_date)
        found_item = search_results[0] if search_results else None

    # If item not found
    if not found_item:
        return jsonify({
            "success": True,
            "found": False,
            "item": None,
            "retrievalSteps": []
        })

    # Generate retrieval steps
    container_id = found_item.get("containerId")
    retrieval_steps = []

    if container_id:
        retrieval_steps = retrieval_algorithm_3d_a_star_rtree(found_item, container_id, items)

    # Log the search operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": user_id,
        "actionType": "search",
        "itemId": found_item.get("itemId"),
        "containerId": container_id,
        "details": {
            "searchTerm": item_name if item_name else f"ID: {item_id}",
            "found": True if found_item else False
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "found": True,
        "item": {
            "itemId": found_item.get("itemId"),
            "name": found_item.get("name"),
            "containerId": container_id,
            "zone": next((c["zone"] for c in current_app.config.get('CONTAINERS', [])
                          if c["containerId"] == container_id), None),
            "position": found_item.get("position")
        },
        "retrievalSteps": retrieval_steps
    })


@search_bp.route('/retrieve', methods=['POST'])
def retrieve():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    item_id = data.get('itemId')
    user_id = data.get('userId', 'anonymous')
    timestamp = data.get('timestamp', datetime.now().isoformat())

    if not item_id:
        return jsonify({"success": False, "error": "Item ID is required"}), 400

    items = current_app.config.get('ITEMS', [])
    item_index = next((i for i, item in enumerate(items) if item.get("itemId") == item_id), None)

    if item_index is None:
        return jsonify({"success": False, "error": "Item not found"}), 404

    # Update usage count
    if "usesRemaining" in items[item_index]:
        items[item_index]["usesRemaining"] -= 1

    # Log the retrieval operation
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": user_id,
        "actionType": "retrieval",
        "itemId": item_id,
        "containerId": items[item_index].get("containerId"),
        "details": {
            "usesRemaining": items[item_index].get("usesRemaining")
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({"success": True})


@search_bp.route('/place', methods=['POST'])
def place():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    item_id = data.get('itemId')
    user_id = data.get('userId', 'anonymous')
    timestamp = data.get('timestamp', datetime.now().isoformat())
    container_id = data.get('containerId')
    position = data.get('position')

    if not item_id or not container_id or not position:
        return jsonify({"success": False, "error": "Item ID, container ID, and position are required"}), 400

    items = current_app.config.get('ITEMS', [])
    item_index = next((i for i, item in enumerate(items) if item.get("itemId") == item_id), None)

    if item_index is None:
        return jsonify({"success": False, "error": "Item not found"}), 404

    # Update item position
    items[item_index]["containerId"] = container_id
    items[item_index]["position"] = position

    # Log the placement operation
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": user_id,
        "actionType": "placement",
        "itemId": item_id,
        "containerId": container_id,
        "details": {
            "position": position
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({"success": True})
