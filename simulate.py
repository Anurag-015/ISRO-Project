from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import uuid

simulate_bp = Blueprint('simulate', __name__)


@simulate_bp.route('/simulate/day', methods=['POST'])
def simulate_day():
    data = request.get_json()

    # Get current date
    current_date_str = current_app.config.get('CURRENT_DATE', '2025-04-06')

    try:
        current_date = datetime.fromisoformat(current_date_str)
    except ValueError:
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")

    # Advance date by one day
    new_date = current_date + timedelta(days=1)
    new_date_str = new_date.isoformat().split('T')[0]

    # Update system date
    current_app.config['CURRENT_DATE'] = new_date_str

    # Process used items
    items_used = data.get('itemsUsed', []) if data else []
    items = current_app.config.get('ITEMS', [])

    # Track changes
    usage_changes = []
    expired_items = []

    # Update usage count for used items
    for used_item in items_used:
        item_id = used_item.get('itemId')
        uses = used_item.get('uses', 1)

        item_index = next((i for i, item in enumerate(items) if item.get("itemId") == item_id), None)

        if item_index is not None:
            item = items[item_index]

            # Update uses remaining
            if "usesRemaining" in item:
                old_uses = item["usesRemaining"]
                item["usesRemaining"] = max(0, old_uses - uses)

                # Track change
                usage_changes.append({
                    "itemId": item_id,
                    "name": item.get("name", ""),
                    "previousUses": old_uses,
                    "newUses": item["usesRemaining"]
                })

    # Check for newly expired items
    for item in items:
        expiry_date = item.get("expiryDate")

        if expiry_date:
            try:
                if datetime.fromisoformat(expiry_date) <= new_date and datetime.fromisoformat(
                        expiry_date) > current_date:
                    expired_items.append({
                        "itemId": item.get("itemId"),
                        "name": item.get("name", ""),
                        "expiryDate": expiry_date
                    })
            except ValueError:
                pass

    # Log the simulation operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "simulation",
        "details": {
            "previousDate": current_date_str,
            "newDate": new_date_str,
            "itemsUsed": len(items_used),
            "newlyExpired": len(expired_items)
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "newDate": new_date_str,
        "changes": {
            "itemsUsed": usage_changes,
            "newlyExpired": expired_items
        }
    })


@simulate_bp.route('/simulate/days', methods=['POST'])
def simulate_days():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    days = data.get('days', 1)
    items_used_daily = data.get('itemsUsedDaily', [])

    if days <= 0:
        return jsonify({"success": False, "error": "Days must be greater than 0"}), 400

    # Get current date
    current_date_str = current_app.config.get('CURRENT_DATE', '2025-04-06')

    try:
        current_date = datetime.fromisoformat(current_date_str)
    except ValueError:
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")

    # Advance date by specified days
    new_date = current_date + timedelta(days=days)
    new_date_str = new_date.isoformat().split('T')[0]

    # Update system date
    current_app.config['CURRENT_DATE'] = new_date_str

    # Process used items
    items = current_app.config.get('ITEMS', [])

    # Track changes
    usage_changes = []
    expired_items = []

    # Update usage count for used items (multiply by days)
    for used_item in items_used_daily:
        item_id = used_item.get('itemId')
        uses_per_day = used_item.get('uses', 1)
        total_uses = uses_per_day * days

        item_index = next((i for i, item in enumerate(items) if item.get("itemId") == item_id), None)

        if item_index is not None:
            item = items[item_index]

            # Update uses remaining
            if "usesRemaining" in item:
                old_uses = item["usesRemaining"]
                item["usesRemaining"] = max(0, old_uses - total_uses)

                # Track change
                usage_changes.append({
                    "itemId": item_id,
                    "name": item.get("name", ""),
                    "previousUses": old_uses,
                    "newUses": item["usesRemaining"],
                    "daysSimulated": days
                })

    # Check for newly expired items
    for item in items:
        expiry_date = item.get("expiryDate")

        if expiry_date:
            try:
                expiry_datetime = datetime.fromisoformat(expiry_date)
                if expiry_datetime <= new_date and expiry_datetime > current_date:
                    expired_items.append({
                        "itemId": item.get("itemId"),
                        "name": item.get("name", ""),
                        "expiryDate": expiry_date
                    })
            except ValueError:
                pass

    # Log the simulation operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "multiDaySimulation",
        "details": {
            "previousDate": current_date_str,
            "newDate": new_date_str,
            "daysSimulated": days,
            "itemsUsedTypes": len(items_used_daily),
            "newlyExpired": len(expired_items)
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "newDate": new_date_str,
        "daysSimulated": days,
        "changes": {
            "itemsUsed": usage_changes,
            "newlyExpired": expired_items
        }
    })
