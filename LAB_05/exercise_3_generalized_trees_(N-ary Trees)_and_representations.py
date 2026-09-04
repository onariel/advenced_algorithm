from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class BinaryCategoryNode:
    category_id: int
    name: str
    post_count: int
    left: Optional['BinaryCategoryNode'] = None   # first child
    right: Optional['BinaryCategoryNode'] = None  # next sibling


@dataclass
class GeneralizedCategoryNode:
    category_id: int
    name: str
    post_count: int
    children: List['GeneralizedCategoryNode'] = field(default_factory=list)
    parent: Optional['GeneralizedCategoryNode'] = None

    def add_child(self, child: 'GeneralizedCategoryNode') -> None:
        child.parent = self
        self.children.append(child)


def binary_to_generalized(root: Optional[BinaryCategoryNode]) -> Optional[GeneralizedCategoryNode]:
    if root is None:
        return None

    node = GeneralizedCategoryNode(root.category_id, root.name, root.post_count)
    child = root.left

    while child:
        converted = binary_to_generalized(child)
        converted.parent = node
        node.children.append(converted)
        child = child.right

    return node


def generalized_to_binary(root: Optional[GeneralizedCategoryNode]) -> Optional[BinaryCategoryNode]:
    if root is None:
        return None

    node = BinaryCategoryNode(root.category_id, root.name, root.post_count)

    if root.children:
        node.left = generalized_to_binary(root.children[0])
        current = node.left

        for child in root.children[1:]:
            current.right = generalized_to_binary(child)
            current = current.right

    return node

def pre_order_generalized(node: Optional[GeneralizedCategoryNode]) -> List[str]:
    if node is None:
        return []

    result = [node.name]
    for child in node.children:
        result.extend(pre_order_generalized(child))
    return result


def post_order_generalized(node: Optional[GeneralizedCategoryNode]) -> List[str]:
    if node is None:
        return []

    result = []
    for child in node.children:
        result.extend(post_order_generalized(child))
    result.append(node.name)
    return result


def level_order_generalized(root: Optional[GeneralizedCategoryNode]) -> List[str]:
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.name)
        queue.extend(node.children)

    return result


def calculate_fan_out(node: Optional[GeneralizedCategoryNode]) -> int:
    if node is None:
        return 0

    max_children = len(node.children)
    for child in node.children:
        max_children = max(max_children, calculate_fan_out(child))
    return max_children


def calculate_height_generalized(node: Optional[GeneralizedCategoryNode]) -> int:
    if node is None:
        return -1
    if not node.children:
        return 0

    return 1 + max(calculate_height_generalized(child) for child in node.children)


def count_nodes_generalized(node: Optional[GeneralizedCategoryNode]) -> int:
    if node is None:
        return 0
    return 1 + sum(count_nodes_generalized(child) for child in node.children)


def count_leaves_generalized(node: Optional[GeneralizedCategoryNode]) -> int:
    if node is None:
        return 0
    if not node.children:
        return 1
    return sum(count_leaves_generalized(child) for child in node.children)


def calculate_branching_factor(root: Optional[GeneralizedCategoryNode]) -> float:
    if root is None:
        return 0.0

    total_children = 0
    non_leaf_nodes = 0
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node.children:
            total_children += len(node.children)
            non_leaf_nodes += 1
            queue.extend(node.children)

    return total_children / non_leaf_nodes if non_leaf_nodes else 0.0


def build_sample_tree() -> GeneralizedCategoryNode:
    tech = GeneralizedCategoryNode(1, 'Technology', 150)
    prog = GeneralizedCategoryNode(2, 'Programming', 85)
    design = GeneralizedCategoryNode(3, 'Design', 65)
    business = GeneralizedCategoryNode(4, 'Business', 70)
    python = GeneralizedCategoryNode(5, 'Python', 42)
    java = GeneralizedCategoryNode(6, 'Java', 30)
    django = GeneralizedCategoryNode(7, 'Django', 18)
    flask = GeneralizedCategoryNode(8, 'Flask', 12)

    tech.add_child(prog)
    tech.add_child(design)
    tech.add_child(business)

    prog.add_child(python)
    prog.add_child(java)

    python.add_child(django)
    python.add_child(flask)

    return tech


if __name__ == '__main__':
    root = build_sample_tree()

    print('Pre-order:', pre_order_generalized(root))
    print('Post-order:', post_order_generalized(root))
    print('Level-order:', level_order_generalized(root))
    print('Fan-out:', calculate_fan_out(root))
    print('Height:', calculate_height_generalized(root))
    print('Nodes:', count_nodes_generalized(root))
    print('Leaves:', count_leaves_generalized(root))
    print('Branching factor:', calculate_branching_factor(root))

    binary_root = generalized_to_binary(root)
    restored_root = binary_to_generalized(binary_root)
    print('Restored Pre-order:', pre_order_generalized(restored_root))
