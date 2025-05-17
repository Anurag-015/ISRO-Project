def knapsack_01_dp(waste_items, max_weight):
    """
    Implements the 0-1 Knapsack (Dynamic Programming) algorithm for waste management.

    Args:
        waste_items: List of waste items
        max_weight: Maximum weight capacity of the return container

    Returns:
        selected_items: List of selected items for return
        total_weight: Total weight of selected items
        total_volume: Total volume of selected items
    """
    n = len(waste_items)

    # If no waste items or no capacity, return empty selection
    if n == 0 or max_weight == 0:
        return [], 0, 0

    # Create weight and value arrays
    weights = [item.get("mass", 0) for item in waste_items]

    # Calculate volume for each item
    volumes = []
    for item in waste_items:
        width = item.get("width", 0)
        depth = item.get("depth", 0)
        height = item.get("height", 0)
        volume = width * depth * height
        volumes.append(volume)

    # Create DP table
    dp = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for w in range(1, max_weight + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(volumes[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Retrieve selected items
    selected_items = []
    total_weight = 0
    total_volume = 0
    w = max_weight

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(waste_items[i - 1])
            total_weight += weights[i - 1]
            total_volume += volumes[i - 1]
            w -= weights[i - 1]

    return selected_items, total_weight, total_volume


def generate_return_plan(waste_items, undocking_container_id, max_weight, all_items):
    """
    Generate a plan for returning waste items.

    Args:
        waste_items: List of waste items
        undocking_container_id: ID of the container for undocking
        max_weight: Maximum weight limit
        all_items: All items in the system

    Returns:
        return_plan: List of steps for waste return
        retrieval_steps: List of retrieval steps
        return_manifest: Manifest for returned items
    """
    # Use Knapsack to select items
    selected_items, total_weight, total_volume = knapsack_01_dp(waste_items, max_weight)

    # Generate return plan
    return_plan = []
    step_counter = 1

    for item in selected_items:
        return_plan.append({
            "step": step_counter,
            "itemId": item["itemId"],
            "itemName": item.get("name", ""),
            "fromContainer": item.get("containerId", ""),
            "toContainer": undocking_container_id
        })
        step_counter += 1

    # Generate retrieval steps for selected items
    retrieval_steps = []
    step_retrieval = 1

    for item in selected_items:
        container_id = item.get("containerId", "")
        if container_id:
            # Find blocking items for this item
            retrieval_result = []

            # Add retrieval steps
            for step in retrieval_result:
                step["step"] = step_retrieval
                retrieval_steps.append(step)
                step_retrieval += 1

    # Generate return manifest
    return_manifest = {
        "undockingContainerId": undocking_container_id,
        "undockingDate": "2025-04-06",  # Current date should be used
        "returnItems": [
            {
                "itemId": item["itemId"],
                "name": item.get("name", ""),
                "reason": item.get("wasteReason", "")
            } for item in selected_items
        ],
        "totalVolume": total_volume,
        "totalWeight": total_weight
    }

    return return_plan, retrieval_steps, return_manifest
