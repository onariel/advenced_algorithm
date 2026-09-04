import random
import math


def count_cross_edges(groupA, groupB, graph):
    setA = set(groupA)
    cross = 0

    for u in range(len(graph)):
        for v in graph[u]:
            # Count only edges from A to B
            if u in setA and v not in setA:
                cross += 1

    return cross


def is_balanced(groupA, groupB, n):
    min_size = math.ceil(0.4 * n)
    return len(groupA) >= min_size and len(groupB) >= min_size


def find_balanced_partition_greedy(graph):
    n = len(graph)
    nodes = list(range(n))

    # Random initial split
    random.shuffle(nodes)

    split = n // 2
    groupA = set(nodes[:split])
    groupB = set(nodes[split:])

    # Ensure balance
    min_size = math.ceil(0.4 * n)
    if len(groupA) < min_size or len(groupB) < min_size:
        return None

    current_cut = count_cross_edges(groupA, groupB, graph)

    improved = True

    while improved:
        improved = False
        best_cut = current_cut
        best_move = None

        # Try moving each node
        for node in range(n):

            # Move A -> B
            if node in groupA:
                if len(groupA) - 1 < min_size:
                    continue

                groupA.remove(node)
                groupB.add(node)

                new_cut = count_cross_edges(groupA, groupB, graph)

                if new_cut < best_cut:
                    best_cut = new_cut
                    best_move = ("A_to_B", node)

                # Undo move
                groupB.remove(node)
                groupA.add(node)

            # Move B -> A
            else:
                if len(groupB) - 1 < min_size:
                    continue

                groupB.remove(node)
                groupA.add(node)

                new_cut = count_cross_edges(groupA, groupB, graph)

                if new_cut < best_cut:
                    best_cut = new_cut
                    best_move = ("B_to_A", node)

                # Undo move
                groupA.remove(node)
                groupB.add(node)

        # Apply best move
        if best_move is not None:
            direction, node = best_move

            if direction == "A_to_B":
                groupA.remove(node)
                groupB.add(node)
            else:
                groupB.remove(node)
                groupA.add(node)

            current_cut = best_cut
            improved = True

    return current_cut, list(groupA), list(groupB)


def find_balanced_partition_local_search(graph, iterations=20):
    best_cut = float("inf")
    best_A = []
    best_B = []

    for _ in range(iterations):
        result = find_balanced_partition_greedy(graph)

        if result is None:
            continue

        cut, A, B = result

        if cut < best_cut:
            best_cut = cut
            best_A = A
            best_B = B

    return best_cut, best_A, best_B


if __name__ == "__main__":


    graph = [
        [1, 3],        
        [0, 2, 4],     
        [1, 5],        
        [0, 4],        
        [1, 3, 5],     
        [2, 4]         
    ]

    print("Running balanced partition local search...\n")

    cut, groupA, groupB = find_balanced_partition_local_search(
        graph,
        iterations=30
    )

    print("Minimum cross edges:", cut)
    print("Group A:", groupA)
    print("Group B:", groupB)
    print("Balanced:",
          is_balanced(groupA, groupB, len(graph)))
