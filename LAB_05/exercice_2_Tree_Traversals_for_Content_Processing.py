import random
class CategoryNode:
    def __init__(self, name,post_count, parent):
        self.category_id = random.randint(1, 100000)
        self.name = name
        self.post_count = post_count
        self.left = None
        self.right = None
        self.parent = parent
        if parent:
            if parent.left:
                if parent.right:
                    print("invalid parent, node already have two child")
                else:
                    parent.right = self
            else:
                parent.left = self

    def add_child_left(self, node):
        self.left = node
    def add_child_right(self, node):
        self.right = node



    def __str__(self):
        return (f"{self.name}, "
                f"count: {self.post_count}, "
                f"parent: {self.parent.name if self.parent else None}, "
                f"left: {self.left.name if self.left else None}, "
                f"right: {self.right.name if self.left else None}")

def in_order(node,original_node = None, solution = []):
    if original_node is None:
        original_node = node
    if node == original_node and node.right in solution:
        return solution
    if node.left is None or node.left in solution:
        if node.right is None:
            solution.append(node)
            return in_order(node.parent, original_node, solution)
        elif node.right in solution:
            return in_order(node.parent, original_node, solution)
        else:
            solution.append(node)
            return in_order(node.right, original_node, solution)
    else:
        return in_order(node.left, original_node, solution)



def in_order_collect(node):
    array = in_order(node, None, [])
    result = []
    if array:
        for node in array:
            result.append(node.name + f"({node.post_count})")
    return result

def in_order_accumulate_posts(node):
    array = in_order(node, None, [])
    total = 0
    for node in array:
        total += node.post_count
    return total

def in_order_find_kth(k, node):
    array = in_order(node, None, [])
    if len(array) < k:
        return None
    else:
        return array[k-1]

def pre_order_export(node):
    original_node = node
    root_new_tree = CategoryNode(node.name, node.post_count, None)
    new_node = root_new_tree
    depth = 0
    result = [node]
    export = f"{node.name}({node.post_count})\n"
    serialized = f"{node.name}({node.post_count}) | "
    while True:
        if original_node == node and (node.right in result or node.right is None):
            break
        if node.left is None or node.left in result:
            if node.right is None or node.right in result:
                depth -= 1
                node = node.parent
                new_node = new_node.parent
            else:
                result.append(node.right)
                node_temp = CategoryNode(node.right.name, node.right.post_count, new_node)
                new_node = node_temp
                depth += 1
                node = node.right
                export += "    "*depth + f"{node.name}({node.post_count})\n"
                serialized += f"{node.name}({node.post_count}) | "
        else:
            result.append(node.left)
            node_temp = CategoryNode(node.left.name, node.left.post_count, new_node)
            new_node = node_temp
            depth += 1
            node = node.left
            export += "    "*depth + f"{node.name}({node.post_count})\n"
            serialized += f"{node.name}({node.post_count}) | "
    print("export: \n",export)
    print("serialized: \n",serialized[:-2])
    return root_new_tree

def post_order(node):
    posts = 0
    nodes = 0
    total_depths = 0
    depth = 0
    result = []
    original = node
    leaves = []
    while True:
        if node == original and (node.right in result or node.right is None):
            break
        if node.left is None or node.left in result:
            if node.right is None or node.right in result:
                if node.right is None and node.left is None:
                    total_depths += depth
                    leaves.append(node)
                    nodes += 1
                result.append(node)
                posts += node.post_count
                node = node.parent
                depth -= 1
            else:
                depth += 1
                node = node.right
        else:
            node = node.left
            depth += 1

    posts += original.post_count
    result.append(original)
    print("total number of posts: ", posts)
    print("average depths: ", total_depths/nodes)
    array = []
    if leaves:
        for node in leaves:
            array.append(node.name + f"({node.post_count})")
    print("leaves: ", array)

def find_most_popular_category(node):
    array = in_order(node, None, [])
    most_popular = array[0]
    for node in array:
        if node.post_count > most_popular.post_count:
            most_popular = node
    return most_popular

Technology = CategoryNode("Technology", 150, None)
Programing = CategoryNode("Programing", 85, Technology)
Python = CategoryNode("Python", 42, Programing)
Django = CategoryNode("Django", 18, Python)
Flask = CategoryNode("Flask", 12, Python)
Java = CategoryNode("Java", 13, Programing)
Design = CategoryNode("Design", 14, Technology)
UI = CategoryNode("UI", 15, Design)
Graphics = CategoryNode("Graphics", 16, Design)

print("\n----------- In order -----------\n")
print("In order collection: ",in_order_collect(Technology))
print("In order accumulation: ",in_order_accumulate_posts(Design))
print("In order kth find: ",in_order_find_kth(5,Programing))
print("\n----------- Pre order -----------\n")
print("\npre order result:")
pre_result = pre_order_export(Technology)
print("\npre order deepcopy:")
pre_order_export(pre_result)

print("\n----------- post order -----------\n")
post_order(Technology)
print("\n----------- traversal-based analytics -----------\n")
print(find_most_popular_category(Technology))