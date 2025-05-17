import random
import numpy as np


def grasp_tabu_search_rearrangement(items, containers, current_placements):
    """
    Implements the GRASP + Tabu Search algorithm for container rearrangement.

    Args:
        items: List of items to be placed
        containers: List of available containers
        current_placements: Current placement of items

    Returns:
        new_placements: New placement recommendations
        rearrangement_steps: List of rearrangement steps
    """
    # Parameters
    max_iterations = 100
    tabu_list_size = 10
    alpha = 0.3  # GRASP parameter

    # Initialize best solution and score
    best_solution = current_placements.copy()
    best_score = evaluate_placement(best_solution, items, containers)

    # Initialize tabu list
    tabu_list = []

    # GRASP + Tabu Search
    for iteration in range(max_iterations):
        # GRASP Construction Phase
        rcl = construct_rcl(items, containers, current_placements, alpha)

        # Select a random solution from RCL
        current_solution = random.choice(rcl) if rcl else best_solution.copy()
        current_score = evaluate_placement(current_solution, items, containers)

        # Tabu Search Local Improvement
        for _ in range(20):  # Number of local search iterations
            # Generate neighborhood
            neighbors = generate_neighbors(current_solution, items, containers)

            # Filter out tabu moves
            non_tabu_neighbors = [n for n in neighbors if not is_tabu(n, tabu_list)]

            if not non_tabu_neighbors:
                continue

            # Select best neighbor
            best_neighbor = None
            best_neighbor_score = float('-inf')

            for neighbor in non_tabu_neighbors:
                score = evaluate_placement(neighbor, items, containers)
                if score > best_neighbor_score:
                    best_neighbor = neighbor
                    best_neighbor_score = score

            # Update current solution
            if best_neighbor_score > current_score:
                tabu_move = get_tabu_move(current_solution, best_neighbor)
                if tabu_move:
                    tabu_list.append(tabu_move)
                    if len(tabu_list) > tabu_list_size:
                        tabu_list.pop(0)

                current_solution = best_neighbor
                current_score = best_neighbor_score

        # Update best solution
        if current_score > best_score:
            best_solution = current_solution
            best_score = current_score

    # Calculate rearrangement steps from current_placements to best_solution
    rearrangement_steps = calculate_rearrangement_steps(current_placements, best_solution)

    return best_solution, rearrangement_steps


def construct_rcl(items, containers, current_placements, alpha):
    """
    Construct Restricted Candidate List (RCL) for GRASP.

    Args:
        items: List of items
        containers: List of containers
        current_placements: Current placement
        alpha: GRASP parameter (0-1)

    Returns:
        rcl: List of candidate solutions
    """
    # This is a simplified implementation
    rcl = []

    # Generate candidate solutions
    for _ in range(10):  # Generate 10 candidates
        candidate = current_placements.copy()

        # Apply random swaps
        num_swaps = random.randint(1, 5)
        for _ in range(num_swaps):
            if len(candidate) >= 2:
                i, j = random.sample(range(len(candidate)), 2)

                # Swap container IDs
                temp_container = candidate[i]["containerId"]
                candidate[i]["containerId"] = candidate[j]["containerId"]
                candidate[j]["containerId"] = temp_container

                # Swap positions
                temp_position = candidate[i]["position"]
                candidate[i]["position"] = candidate[j]["position"]
                candidate[j]["position"] = temp_position

        rcl.append(candidate)

    return rcl


def generate_neighbors(current_solution, items, containers):
    """
    Generate neighboring solutions for Tabu Search.

    Args:
        current_solution: Current placement
        items: List of items
        containers: List of containers

    Returns:
        neighbors: List of neighboring solutions
    """
    neighbors = []

    # Generate neighbors by swapping pairs of items
    if len(current_solution) >= 2:
        for i in range(len(current_solution)):
            for j in range(i + 1, len(current_solution)):
                neighbor = current_solution.copy()

                # Swap container IDs
                temp_container = neighbor[i]["containerId"]
                neighbor[i]["containerId"] = neighbor[j]["containerId"]
                neighbor[j]["containerId"] = temp_container

                # Swap positions
                temp_position = neighbor[i]["position"]
                neighbor[i]["position"] = neighbor[j]["position"]
                neighbor[j]["position"] = temp_position

                neighbors.append(neighbor)

    return neighbors


def evaluate_placement(placement, items, containers):
    """
    Evaluate a placement solution.

    Args:
        placement: Placement solution
        items: List of items
        containers: List of containers

    Returns:
        score: Evaluation score
    """
    # This is a simplified scoring function
    score = 0

    # Create a mapping from item ID to item data
    item_map = {item["itemId"]: item for item in items}

    # Score based on priority and preferred zone
    for p in placement:
        item_id = p["itemId"]
        container_id = p["containerId"]

        if item_id in item_map:
            item = item_map[item_id]

            # Find container
            container = next((c for c in containers if c["containerId"] == container_id), None)

            if container:
                # Priority score (higher priority = higher score)
                score += item.get("priority", 0)

                # Preferred zone score
                if container["zone"] == item.get("preferredZone", ""):
                    score += 50

    return score


def is_tabu(solution, tabu_list):
    """
    Check if a solution is in the tabu list.

    Args:
        solution: Solution to check
        tabu_list: List of tabu moves

    Returns:
        True if tabu, False otherwise
    """
    for tabu_move in tabu_list:
        if set(tabu_move) == set((p["itemId"], p["containerId"]) for p in solution):
            return True

    return False


def get_tabu_move(current_solution, new_solution):
    """
    Get the tabu move between two solutions.

    Args:
        current_solution: Current placement
        new_solution: New placement

    Returns:
        tabu_move: Tabu move representation
    """
    # Create a set of (itemId, containerId) pairs for each solution
    current_set = set((p["itemId"], p["containerId"]) for p in current_solution)
    new_set = set((p["itemId"], p["containerId"]) for p in new_solution)

    # Find differences
    differences = current_set.symmetric_difference(new_set)

    if differences:
        return tuple(differences)
    else:
        return None


def calculate_rearrangement_steps(current_placements, new_placements):
    """
    Calculate steps to rearrange from current to new placements.

    Args:
        current_placements: Current placement
        new_placements: New placement

    Returns:
        steps: List of rearrangement steps
    """
    steps = []
    step_counter = 1

    # Create mapping of item ID to placement
    current_map = {p["itemId"]: p for p in current_placements}
    new_map = {p["itemId"]: p for p in new_placements}

    # Find items that need to be moved
    for item_id, new_placement in new_map.items():
        if item_id in current_map:
            current_placement = current_map[item_id]

            # If placement has changed
            if (current_placement["containerId"] != new_placement["containerId"] or
                    current_placement["position"] != new_placement["position"]):
                # Step 1: Remove the item from current position
                steps.append({
                    "step": step_counter,
                    "action": "remove",
                    "itemId": item_id,
                    "fromContainer": current_placement["containerId"],
                    "fromPosition": current_placement["position"],
                    "toContainer": None,
                    "toPosition": None
                })
                step_counter += 1

                # Step 2: Place the item in new position
                steps.append({
                    "step": step_counter,
                    "action": "place",
                    "itemId": item_id,
                    "fromContainer": None,
                    "fromPosition": None,
                    "toContainer": new_placement["containerId"],
                    "toPosition": new_placement["position"]
                })
                step_counter += 1

    # Handle new items that weren't in current placement
    for item_id, new_placement in new_map.items():
        if item_id not in current_map:
            steps.append({
                "step": step_counter,
                "action": "place",
                "itemId": item_id,
                "fromContainer": None,
                "fromPosition": None,
                "toContainer": new_placement["containerId"],
                "toPosition": new_placement["position"]
            })
            step_counter += 1

    return steps
