from flask import Blueprint, request, jsonify, current_app
from algorithms.waste_management import knapsack_01_dp, generate_return_plan
from datetime import datetime
import uuid

waste_bp = Blueprint('waste', __name__)


@waste_bp.route('/waste/identify', methods=['GET'])
def identify_waste():
    items = current_app.config.get('ITEMS', [])
    current_date = current_app.config.get('CURRENT_DATE', '2025-04-06')

    # Identify waste items
    waste_items = []

    for item in items:
        is_waste, reason = is_item_waste(item, current_date)

        if is_waste:
            waste_items.append({
                "itemId": item["itemId"],
                "name": item.get("name", ""),
                "reason": reason,
                "containerId": item.get("containerId"),
                "position": item.get("position")
            })

    # Log the waste identification operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "wasteIdentification",
        "details": {
            "numWasteItems": len(waste_items),
            "currentDate": current_date
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "wasteItems": waste_items
    })


@waste_bp.route('/waste/return-plan', methods=['POST'])
def return_plan():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    undocking_container_id = data.get('undockingContainerId')
    undocking_date = data.get('undockingDate')
    max_weight = data.get('maxWeight', 1000)  # Default to 1000 kg if not specified

    if not undocking_container_id or not undocking_date:
        return jsonify({"success": False, "error": "Undocking container ID and date are required"}), 400

    items = current_app.config.get('ITEMS', [])
    current_date = current_app.config.get('CURRENT_DATE', '2025-04-06')

    # Identify waste items
    waste_items = []

    for item in items:
        is_waste, reason = is_item_waste(item, current_date)

        if is_waste:
            waste_item = item.copy()
            waste_item["wasteReason"] = reason
            waste_items.append(waste_item)

    # Generate return plan
    return_plan, retrieval_steps, return_manifest = generate_return_plan(
        waste_items, undocking_container_id, max_weight, items
    )

    # Log the return plan operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "returnPlan",
        "containerId": undocking_container_id,
        "details": {
            "undockingDate": undocking_date,
            "maxWeight": max_weight,
            "numItemsSelected": len(return_manifest["returnItems"])
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "returnPlan": return_plan,
        "retrievalSteps": retrieval_steps,
        "returnManifest": return_manifest
    })


@waste_bp.route('/waste/complete-undocking', methods=['POST'])
def complete_undocking():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    undocking_container_id = data.get('undockingContainerId')
    timestamp = data.get('timestamp', datetime.now().isoformat())

    if not undocking_container_id:
        return jsonify({"success": False, "error": "Undocking container ID is required"}), 400

    items = current_app.config.get('ITEMS', [])

    # Find items in undocking container
    items_in_container = [i for i in items if i.get("containerId") == undocking_container_id]

    # Remove items from the system
    items_removed = 0
    for item in items_in_container:
        if item in items:
            items.remove(item)
            items_removed += 1

    # Update items in the system
    current_app.config['ITEMS'] = items

    # Log the undocking operation
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "undocking",
        "containerId": undocking_container_id,
        "details": {
            "itemsRemoved": items_removed
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "itemsRemoved": items_removed
    })


def is_item_waste(item, current_date):
    """
    Check if an item is considered waste.

    Args:
        item: Item to check
        current_date: Current system date

    Returns:
        is_waste: True if item is waste, False otherwise
        reason: Reason for waste status
    """
    # Check expiry date
    if item.get("expiryDate"):
        try:
            if datetime.fromisoformat(current_date) > datetime.fromisoformat(item["expiryDate"]):
                return True, "Expired"
        except ValueError:
            pass

    # Check usage limit
    if item.get("usesRemaining", item.get("usageLimit", 1)) <= 0:
        return True, "Out of Uses"

    return False, None
