from itertools import combinations


# ---------------------------------------------------------------------------
# 1. is_valid_coverage
# ---------------------------------------------------------------------------

def is_valid_coverage(selected_users: list, graph: dict) -> bool:
    """
    Complexity: O(N + E)
    """
    covered = set()

    # Mark every selected node as covered
    for u in selected_users:
        covered.add(u)

    # Mark every neighbor of a selected node as covered
    for u in selected_users:
        for v in graph.get(u, []):
            covered.add(v)

    # Every node in the graph must be covered
    for node in graph:
        if node not in covered:
            return False

    return True


# ---------------------------------------------------------------------------
# 2. find_minimum_coverage
# ---------------------------------------------------------------------------

def find_minimum_coverage(graph: dict) -> tuple:
    """
    Complexity: O(2^N * (N + E))  — correct for N ≤ 20
    """
    nodes = list(graph.keys())
    n = len(nodes)

    size = n + 1                    
    list_of_selected_users = []

    for selected_num in range(1, n + 1):
        all_candidates = combinations(nodes, selected_num)

        for selected_users in all_candidates:
            if len(selected_users) >= size:
                continue

            if is_valid_coverage(list(selected_users), graph):
                size = len(selected_users)
                list_of_selected_users = list(selected_users)
                return (size, list_of_selected_users)

    return (size, list_of_selected_users)


# ---------------------------------------------------------------------------
# Helper for find_fast_coverage
# ---------------------------------------------------------------------------

def _count_covered(u, uncovered: set, graph: dict) -> int:
    """
    Count how many currently uncovered nodes would be dominated
    by selecting node u  (u itself + its uncovered neighbours).

    Complexity: O(deg(u))
    """
    count = 1 if u in uncovered else 0
    for v in graph.get(u, []):
        if v in uncovered:
            count += 1
    return count


# ---------------------------------------------------------------------------
# 3. find_fast_coverage
# ---------------------------------------------------------------------------

def find_fast_coverage(graph: dict) -> tuple:
    """
    Complexity: O(N * (N + E))
    """
    uncovered_nodes = set(graph.keys())
    list_of_selected_users = []

    while uncovered_nodes:
        best_node = None
        max_coverage = -1

        for u in graph:
            current_gain = _count_covered(u, uncovered_nodes, graph)
            if current_gain > max_coverage:
                max_coverage = current_gain
                best_node = u

        list_of_selected_users.append(best_node)

        uncovered_nodes.discard(best_node)
        for neighbor in graph.get(best_node, []):
            uncovered_nodes.discard(neighbor)

    size = len(list_of_selected_users)
    return (size, list_of_selected_users)


if __name__ == '__main__':
    print("=" * 60)
    print("Start running test cases")
    print("=" * 60)


    print("\nTest Case 1: Single Node Graph")
    graph1 = {1: []}
    print("is_valid_coverage test：", is_valid_coverage([1], graph1))  # True
    print("function2：", find_minimum_coverage(graph1))
    print("function3：", find_fast_coverage(graph1))

  
    print("\nTest Case 2: Two Connected Nodes")
    graph2 = {1: [2], 2: [1]}
    print("is_valid_coverage test：", is_valid_coverage([1], graph2))  # True
    print("function2：", find_minimum_coverage(graph2))
    print("function3：", find_fast_coverage(graph2))


    print("\nTest Case 3: Three-Node Chain Structure")
    graph3 = {1: [2], 2: [1, 3], 3: [2]}
    print("is_valid_coverage test：", is_valid_coverage([2], graph3))  # True
    print("function2：", find_minimum_coverage(graph3))
    print("function3：", find_fast_coverage(graph3))

  
    print("\nTest Case 4: Star Graph")
    graph4 = {1: [2], 2: [1, 3, 4], 3: [2], 4: [2]}
    print("is_valid_coverage test：", is_valid_coverage([2], graph4))  # True
    print("function2：", find_minimum_coverage(graph4))
    print("function3：", find_fast_coverage(graph4))


    print("\nTest Case 5: Invalid Coverage Verification")
    graph5 = {1: [2], 2: [1], 3: [2]}
    print("Select [1], whether to cover all nodes：", is_valid_coverage([1], graph5))  # False（3未覆盖）
    print("Select [2], whether to cover all nodes：", is_valid_coverage([2], graph5))  # True


    print("\nTest Case 6: Quadrilateral Graph")
    graph6 = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
    print("function2：", find_minimum_coverage(graph6))
    print("function3：", find_fast_coverage(graph6))

    print("\n" + "=" * 60)
    print("all finished")
    print("=" * 60)