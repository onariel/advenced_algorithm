
def is_valid_labeling(labeling, graph):
    """
    labeling[i] = color assigned to node i
    graph = adjacency list
    """
    for u in range(len(graph)):
        for v in graph[u]:
            if labeling[u] == labeling[v]:
                return False
    return True


def is_safe(node, color, labeling, graph):
    for neighbor in graph[node]:
        if labeling[neighbor] == color:
            return False
    return True



def color_graph(index, nodes, k, labeling, graph):
    # All nodes colored successfully
    if index == len(nodes):
        return True

    node = nodes[index]

    # Try every possible color
    for color in range(k):
        if is_safe(node, color, labeling, graph):
            labeling[node] = color

            # Recurse
            if color_graph(index + 1, nodes, k, labeling, graph):
                return True

            # Backtrack
            labeling[node] = -1

    return False


def assign_labels(k, graph):
    n = len(graph)

    # Initialize all nodes as uncolored
    labeling = [-1] * n

    # Optimization:
    # Sort nodes by descending degree
    nodes = sorted(range(n), key=lambda x: len(graph[x]), reverse=True)

    success = color_graph(0, nodes, k, labeling, graph)

    return success, labeling



def find_min_labels(graph):
    n = len(graph)

    for k in range(1, n + 1):
        success, labeling = assign_labels(k, graph)

        if success:
            return k, labeling

    return None


# Example test

if __name__ == "__main__":


    graph = [
        [1, 2],        
        [0, 2, 3],     
        [0, 1, 3],    
        [1, 2]        
    ]

    print("Testing minimum labeling...\n")

    min_k, labeling = find_min_labels(graph)

    print("Minimum labels needed:", min_k)
    print("Labeling:", labeling)

    print("\nValid labeling?",
          is_valid_labeling(labeling, graph))
