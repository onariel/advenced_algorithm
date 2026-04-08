
class CategoryNode:
    def __init__(self, category_id: int, name: str, post_count: int):
        self.category_id = category_id  
        self.name = name              
        self.post_count = post_count    
        self.left = None               
        self.right = None               
        self.parent = None              

# Height of trees
def calculate_height(node):
    if node == None:
        return -1
    left_h = calculate_height(node.left)
    right_h = calculate_height(node.right)
    return max(left_h, right_h) + 1

# Find the target node
def find_category(target_id, node):
    if node is None:
        return None
    if node.category_id == target_id:
        return node
    left_result = find_category(target_id, node.left)
    if left_result:
        return left_result
    return find_category(target_id, node.right)

# node height
def calculate_node_height(node, target_id):
    target_node = find_category(target_id, node)
    if target_node == None:
        return -1
    return calculate_height(target_node)

# find the total number of nodes
def count_nodes(node):
    if node == None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

# find the total number of leaves
def count_leaves(node):
    if node == None:
        return 0
    if node.left == None and node.right == None:
        return 1
    return count_leaves(node.right) + count_leaves(node.left)

# tress balance
def is_balanced(node):
    if node == None:
        return True
    left_h = calculate_height(node.left)
    right_h = calculate_height(node.right)
    if abs(left_h - right_h) > 1:
        return False
    return is_balanced(node.left) and is_balanced(node.right)

# Determine if a binary tree is full
def is_full_binary_tree(node):
    if node == None:
        return True
    if node.left == None and node.right == None:
        return True
    if node.left != None and node.right != None:
        return is_full_binary_tree(node.left) and is_full_binary_tree(node.right)
    return False

# Determine a perfect tree
def is_perfect_binary_tree(node):
    height = calculate_height(node)
    node_count = count_nodes(node)
    perfect_count = 2 ** (height + 1) - 1
    return node_count == perfect_count

# Auxiliary function
def is_complete_helper(node, index, total_nodes):
    if node == None:
        return False
    if index > total_nodes:
        return False
    return is_complete_helper(node.left, index * 2, total_nodes) and is_complete_helper(node.right, index * 2 + 1, total_nodes)

# Determine if a binary tree is complete
def is_complete_binary_tree(node):
    total = count_nodes(node)
    return is_complete_helper(node, 1, total)

# Find category nodes by ID
def find_category(target_id, node):
    if node == None:
        return None
    if node.category_id == target_id:
        return node
    left_result = find_category(target_id, node.left)
    if left_result != None:
        return left_result
    return find_category(target_id, node.right)

# Find the path from the target node to the root node.
def find_path_to_root(target_id, node):
    path = []
    target_node = find_category(target_id, node)
    if target_node == None:
        return path
    current = target_node
    while current != None:
        path.append(current.name)
        current = current.parent
    return path


def find_category_by_name(name, node):
    if node == None:
        return None
    if node.name == name:
        return node
    left = find_category_by_name(name, node.left)
    if left:
        return left
    return find_category_by_name(name, node.right)


# Find the lowest common ancestor of two nodes.
def lowest_common_ancestor(id1, id2, node):
    path1 = find_path_to_root(id1, node)
    path2 = find_path_to_root(id2, node)
    if len(path1) == 0 or len(path2) == 0:
        return None
    i = len(path1) - 1
    j = len(path2) - 1
    lca = None
    while i >= 0 and j >= 0 and path1[i] == path2[j]:
        lca = path1[i]
        i = i - 1
        j = j - 1
    if lca != None:
        return find_category_by_name(lca, node)
    return None




# Test cases
# creat tree
tech = CategoryNode(1, "Technology", 150)
prog = CategoryNode(2, "Programming", 85)
design = CategoryNode(3, "Design", 65)
python = CategoryNode(4, "Python", 42)
java = CategoryNode(5, "Java", 30)
django = CategoryNode(6, "Django", 18)
flask = CategoryNode(7, "Flask", 12)
ux = CategoryNode(8, "UI/UX", 38)
graphics = CategoryNode(9, "Graphics", 22)

tech.left = prog
tech.right = design
prog.left = python
prog.right = java
python.left = django
python.right = flask
design.left = ux
design.right = graphics

prog.parent = tech
design.parent = tech
python.parent = prog
java.parent = prog
django.parent = python
flask.parent = python
ux.parent = design
graphics.parent = design

root = tech

#  calculate_height
print("test calculate_height:")
result = calculate_height(root)
print(f"  height of tree: {result}")
assert result == 3, f"exceped 3, result: {result}"

#  find_category
print("test find_category:")
node = find_category(4, root)
print(f"  find node which ID = 4: {node.name if node else None}")
assert node is not None and node.name == "Python", "python"
print("  test find_category passed\n")

# test calculate_node_height
print("test calculate_node_height:")
result = calculate_node_height(root, 5)  # Java
print(f"  Java node height: {result}")
assert result == 0, f"excepted 0, result: {result}"
print("  calculate_node_height passed\n")

# test count_nodes
print("test count_nodes:")
result = count_nodes(root)
print(f"  total nodes: {result}")
assert result == 9, f"excepted 9, result {result}"
print("  passed\n")

# test count_leaves
print("test count_leaves:")
result = count_leaves(root)
print(f"  node leaves: {result}")
assert result == 5, f"excepted 5, result {result}"
print("  passed\n")

# test is_balanced
print("test is_balanced:")
result = is_balanced(root)
print(f"  tree is balanced: {result}")
assert result == True, "tree should be balanced"
print("  passed\n")

# test is_full_binary_tree
print("test is_full_binary_tree:")
result = is_full_binary_tree(root)
print(f"  Is full binary tree: {result}")
assert result == True, "false"
print("  passed\n")

# test is_perfect_binary_tree
print("test is_perfect_binary_tree:")
result = is_perfect_binary_tree(root)
print(f"  Is perfect binary tree: {result}")
assert result == False, "trees should not perfect"
print("  passed\n")

# test is_complete_binary_tree
print("test is_complete_binary_tree:")
result = is_complete_binary_tree(root)
print(f"  Tree is complete binary tree: {result}")
assert result == False, "false"
print("  passed\n")

# test find_path_to_root
print("test find_path_to_root:")
result = find_path_to_root(6, root)  # Django
print(f"  Django path to root: {result}")
expected = ["Django", "Python", "Programming", "Technology"]
assert result == expected, f"excepted {expected}, result {result}"
print("  passed\n")

# test lowest_common_ancestor
print("test lowest_common_ancestor:")
lca_node = lowest_common_ancestor(6, 5, root)  # Django and Java
result = lca_node.name if lca_node else None
print(f"  Django and Java lca: {result}")
assert result == "Programming", f"excepted Programming, result {result}"
print("  passed\n")
