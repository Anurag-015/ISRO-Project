from flask import Blueprint, request, jsonify, current_app, send_file
import csv
import io
import uuid
from datetime import datetime

import_export_bp = Blueprint('import_export', __name__)


@import_export_bp.route('/import/items', methods=['POST'])
def import_items():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"success": False, "error": "File must be a CSV"}), 400

    items = []
    errors = []
    row_number = 0

    try:
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)

        # Get header row
        header = next(csv_reader)
        row_number = 1

        # Map header indices
        header_map = {
            "itemId": header.index("Item ID") if "Item ID" in header else None,
            "name": header.index("Name") if "Name" in header else None,
            "width": header.index("Width (cm)") if "Width (cm)" in header else None,
            "depth": header.index("Depth (cm)") if "Depth (cm)" in header else None,
            "height": header.index("Height (cm)") if "Height (cm)" in header else None,
            "mass": header.index("Mass (kg)") if "Mass (kg)" in header else None,
            "priority": header.index("Priority (1-100)") if "Priority (1-100)" in header else None,
            "expiryDate": header.index("Expiry Date (ISO Format)") if "Expiry Date (ISO Format)" in header else None,
            "usageLimit": header.index("Usage Limit") if "Usage Limit" in header else None,
            "preferredZone": header.index("Preferred Zone") if "Preferred Zone" in header else None
        }

        # Validate required headers
        required_headers = ["itemId", "name", "width", "depth", "height"]
        missing_headers = [header for header in required_headers if header_map[header] is None]

        if missing_headers:
            return jsonify({
                "success": False,
                "error": f"Missing required headers: {', '.join(missing_headers)}"
            }), 400

        # Process each row
        for row in csv_reader:
            row_number += 1

            try:
                item = {
                    "itemId": row[header_map["itemId"]],
                    "name": row[header_map["name"]],
                    "width": float(row[header_map["width"]]),
                    "depth": float(row[header_map["depth"]]),
                    "height": float(row[header_map["height"]])
                }

                # Optional fields
                if header_map["mass"] is not None:
                    item["mass"] = float(row[header_map["mass"]])

                if header_map["priority"] is not None:
                    item["priority"] = int(row[header_map["priority"]])

                if header_map["expiryDate"] is not None and row[header_map["expiryDate"]]:
                    item["expiryDate"] = row[header_map["expiryDate"]]

                if header_map["usageLimit"] is not None:
                    item["usageLimit"] = int(row[header_map["usageLimit"]])
                    item["usesRemaining"] = int(row[header_map["usageLimit"]])

                if header_map["preferredZone"] is not None:
                    item["preferredZone"] = row[header_map["preferredZone"]]

                items.append(item)

            except (ValueError, IndexError) as e:
                errors.append({
                    "row": row_number,
                    "message": str(e)
                })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing CSV: {str(e)}"
        }), 400

    # Update in-memory database
    current_app.config['ITEMS'] = items

    # Log the import operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "importItems",
        "details": {
            "itemsImported": len(items),
            "errors": len(errors)
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "itemsImported": len(items),
        "errors": errors
    })


@import_export_bp.route('/import/containers', methods=['POST'])
def import_containers():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"success": False, "error": "File must be a CSV"}), 400

    containers = []
    errors = []
    row_number = 0

    try:
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)

        # Get header row
        header = next(csv_reader)
        row_number = 1

        # Map header indices
        header_map = {
            "zone": header.index("Zone") if "Zone" in header else None,
            "containerId": header.index("Container ID") if "Container ID" in header else None,
            "width": header.index("Width(cm)") if "Width(cm)" in header else None,
            "depth": header.index("Depth(cm)") if "Depth(cm)" in header else None,
            "height": header.index("Height(height)") if "Height(height)" in header else None
        }

        # Validate required headers
        required_headers = ["zone", "containerId", "width", "depth", "height"]
        missing_headers = [header for header in required_headers if header_map[header] is None]

        if missing_headers:
            return jsonify({
                "success": False,
                "error": f"Missing required headers: {', '.join(missing_headers)}"
            }), 400

        # Process each row
        for row in csv_reader:
            row_number += 1

            try:
                container = {
                    "zone": row[header_map["zone"]],
                    "containerId": row[header_map["containerId"]],
                    "width": float(row[header_map["width"]]),
                    "depth": float(row[header_map["depth"]]),
                    "height": float(row[header_map["height"]])
                }

                containers.append(container)

            except (ValueError, IndexError) as e:
                errors.append({
                    "row": row_number,
                    "message": str(e)
                })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing CSV: {str(e)}"
        }), 400

    # Update in-memory database
    current_app.config['CONTAINERS'] = containers

    # Log the import operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "importContainers",
        "details": {
            "containersImported": len(containers),
            "errors": len(errors)
        }
    }
    current_app.config['LOGS'].append(log)

    return jsonify({
        "success": True,
        "containersImported": len(containers),
        "errors": errors
    })


@import_export_bp.route('/export/arrangement', methods=['GET'])
def export_arrangement():
    items = current_app.config.get('ITEMS', [])

    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Item ID", "Container ID", "Coordinates (W1,D1,H1),(W2,D2,H2)"])

    # Write items
    for item in items:
        if "containerId" in item and "position" in item:
            coordinates = (
                f"({item['position']['startCoordinates']['width']},"
                f"{item['position']['startCoordinates']['depth']},"
                f"{item['position']['startCoordinates']['height']}),"
                f"({item['position']['endCoordinates']['width']},"
                f"{item['position']['endCoordinates']['depth']},"
                f"{item['position']['endCoordinates']['height']})"
            )

            writer.writerow([item["itemId"], item["containerId"], coordinates])

    # Prepare response
    output.seek(0)

    # Log the export operation
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log = {
        "logId": log_id,
        "timestamp": timestamp,
        "userId": "system",
        "actionType": "exportArrangement",
        "details": {
            "itemsExported": sum(1 for item in items if "containerId" in item and "position" in item)
        }
    }
    current_app.config['LOGS'].append(log)

    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='arrangement.csv'
    )
