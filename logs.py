from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    # Get query parameters
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    item_id = request.args.get('itemId')
    user_id = request.args.get('userId')
    action_type = request.args.get('actionType')

    # Get logs from in-memory database
    logs = current_app.config.get('LOGS', [])

    # Apply filters
    filtered_logs = logs

    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) >= start]
        except ValueError:
            pass

    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) <= end]
        except ValueError:
            pass

    if item_id:
        filtered_logs = [log for log in filtered_logs if log.get("itemId") == item_id]

    if user_id:
        filtered_logs = [log for log in filtered_logs if log.get("userId") == user_id]

    if action_type:
        filtered_logs = [log for log in filtered_logs if log.get("actionType") == action_type]

    # Sort logs by timestamp (newest first)
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)

    return jsonify({
        "success": True,
        "logs": filtered_logs
    })
