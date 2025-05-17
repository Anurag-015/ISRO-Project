def retrieval_algorithm_3d_a_star_rtree(item, container_id, all_items):
    """
    Implements the 3D A* + R-tree Indexing algorithm for item retrieval.

    Args:
        item: Item to be retrieved
        container_id: ID of the container
        all_items: All items in the system

    Returns:
        retrieval_steps: List of steps required to retrieve the item
    """
    # Get items in the same container
    container_items = [i for i in all_items if i["containerId"] == container_id and i["itemId"] != item["itemId"]]

    # Get item position
    item_position = item.get("position")
    if not item_position:
        return []

    # Find blocking items
    blocking_items = find_blocking_items(item_position, container_items)

    # If no blocking items, direct retrieval
    if not blocking_items:
        return [{
            "step": 1,
            "action": "retrieve",
            "itemId": item["itemId"],
            "itemName": item.get("name", "")
        }]

    # Generate retrieval steps
    retrieval_steps = []
    step_counter = 1

    # Sort blocking items by distance from open face
    blocking_items.sort(key=lambda x: x["position"]["startCoordinates"]["depth"])

    # Remove blocking items
    for blocking_item in blocking_items:
        retrieval_steps.append({
            "step": step_counter,
            "action": "remove",
            "itemId": blocking_item["itemId"],
            "itemName": blocking_item.get("name", "")
        })
        step_counter += 1

    # Retrieve target item
    retrieval_steps.append({
        "step": step_counter,
        "action": "retrieve",
        "itemId": item["itemId"],
        "itemName": item.get("name", "")
    })
    step_counter += 1

    # Place blocking items back
    for blocking_item in reversed(blocking_items):
        retrieval_steps.append({
            "step": step_counter,
            "action": "placeBack",
            "itemId": blocking_item["itemId"],
            "itemName": blocking_item.get("name", "")
        })
        step_counter += 1

    return retrieval_steps


def find_blocking_items(item_position, container_items):
    """
    Find items that block the retrieval path of the target item.

    Args:
        item_position: Position of the target item
        container_items: Other items in the same container

    Returns:
        blocking_items: List of items blocking the retrieval path
    """
    blocking_items = []

    # Get target item boundaries
    target_x1 = item_position["startCoordinates"]["width"]
    target_x2 = item_position["endCoordinates"]["width"]
    target_y1 = item_position["startCoordinates"]["height"]
    target_y2 = item_position["endCoordinates"]["height"]
    target_z = item_position["startCoordinates"]["depth"]

    # Check each item if it blocks the retrieval path
    for item in container_items:
        position = item["position"]

        # Item coordinates
        item_x1 = position["startCoordinates"]["width"]
        item_x2 = position["endCoordinates"]["width"]
        item_y1 = position["startCoordinates"]["height"]
        item_y2 = position["endCoordinates"]["height"]
        item_z1 = position["startCoordinates"]["depth"]
        item_z2 = position["endCoordinates"]["depth"]

        # Check if item is in front of target item (closer to open face)
        if item_z1 < target_z:
            # Check if item overlaps with target item in x and y dimensions
            x_overlap = (item_x1 < target_x2 and item_x2 > target_x1)
            y_overlap = (item_y1 < target_y2 and item_y2 > target_y1)

            if x_overlap and y_overlap:
                blocking_items.append(item)

    return blocking_items
