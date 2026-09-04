from cmath import inf

from exo3_usernames import usernames
import random

class user:
    def __init__(self, name):
        self.name = name
        self.user_id = random.randint(1, 10000)

class trie_node:
    def __init__(self, letter, parent):
        self.children = []
        self.letter = letter
        self.is_end_username = False
        self.user_id = 0
        self.parent = parent

    def add_child(self, letter, parent=None):
        self.children.append(trie_node(letter,parent))

    def end_username(self):
        self.is_end_username = True

class trie:
    def __init__(self):
        self.root = trie_node('',None)

    def search_trie(self, user_name, letter = None):
        if letter is None:
            letter = self.root
        if user_name == '':
            if not letter.is_end_username:
                return None
            else:
                return letter.user_id
        if not letter.children:
            return None
        for i in letter.children:
            if i.letter == user_name[0]:
                return self.search_trie(user_name[1:], i)
        return None

    def insert(self, user):
        path = ""
        curr_letter = self.root
        for letters in user.name:
            if not curr_letter.children == []:
                letter_found = False
                for n in curr_letter.children:
                    if n.letter == letters:
                        letter_found = True
                        curr_letter = n
                        break
                if not letter_found:
                    curr_letter.children.append(trie_node(letters, curr_letter))
                    curr_letter = curr_letter.children[-1]
            else:
                curr_letter.children.append(trie_node(letters, curr_letter))
                curr_letter = curr_letter.children[0]
        curr_letter.user_id = user.user_id
        curr_letter.is_end_username = True

    def start_with(self, prefix, node = None):
        if node is None:
            node = self.root
        if prefix == '':
            if not node.children:
                return False
            else:
                return True
        if not node.children:
            return False
        return self.start_with(prefix[1:], node)

    def autocomplete(self, prefix, max_result = 10):
        result = []
        node = self.root
        for letters in prefix:
            letter_found = False
            for n in node.children:
                if n.letter == letters:
                    node = n
                    letter_found = True
                    break
            if not letter_found:
                return result
        nodes_to_visit = [(node, "")]
        while nodes_to_visit and len(result) < max_result:
            node, string = nodes_to_visit.pop(0)
            for n in node.children:
                nodes_to_visit.append((n, string + node.letter))
            if node.is_end_username:
                result.append(string[1:] + node.letter)
        return result

    def count_words(self):
        count = 0
        nodes = [self.root]
        while nodes:
            node = nodes.pop(0)
            for n in node.children:
                nodes.append(n)
            if node.is_end_username:
                count += 1
        return count

    def get_height(self):
        max_length = 0
        nodes = [(self.root,0)]
        while nodes:
            node,height = nodes.pop(0)
            for n in node.children:
                nodes.append((n,height + 1))
            if height > max_length:
                max_length = height
        return max_length

    def get_total_nodes(self):
        count = -1
        nodes = [self.root]
        while nodes:
            node = nodes.pop(0)
            count += 1
            for n in node.children:
                nodes.append(n)
        return count

    def delete(self, username):
        if not self.search_trie(username):
            return "user not found"
        node = self.root
        for letter in username:
            for n in node.children:
                if n.letter == letter:
                    node = n
                    break
        node.is_end_username = False
        while not node.children:
            node_parent = node.parent
            node.parent = None
            for i in range(len(node_parent.children)):
                if node == node_parent.children[i]:
                    node_parent.children.pop(i)
                    break
            node = node_parent
        return "user deleted"

    def print_trie(self):
        def _print_node(node, prefix="", is_last=True, is_root=True):
            if is_root:
                print("(root)")
            else:
                connector = "└── " if is_last else "├── "
                label = f"{node.letter}"
                if node.is_end_username:
                    label += "  ●"
                print(prefix + connector + label)

            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                _print_node(child, child_prefix, i == len(node.children) - 1, False)

        _print_node(self.root)

class segment_tree_node:
    def __init__(self, value, index_min, index_max, parent = None):
        self.value = value
        self.index_min = index_min
        self.index_max = index_max
        self.left = None
        self.right = None
        self.parent = parent

    def add_child(self, node):
        if self.left is None:
            self.left = node
        else:
            self.right = node

    def __str__(self):
        return f"[{self.index_min}:{self.index_max}] value: {self.value}, left : [{self.left.index_min if not self.left is None else None},{self.left.index_max if not self.left is None else None}] right: [{self.right.index_min if not self.right is None else None},{self.right.index_max if not self.right is None else None}]"

class segment_tree:
    def __init__(self):
        self.root = None

    def build(self,array):
        index_min = 0
        index_max = len(array)-1
        node_parent = segment_tree_node(sum(array), index_min, index_max)
        self.root = node_parent
        difference_min_max = (index_max - index_min)//2
        node_to_create = [(node_parent, index_min + difference_min_max+1, index_max),
                          (node_parent, index_min, index_min + difference_min_max)]
        while node_to_create:
            parent_node, index_min, index_max = node_to_create.pop(-1)
            if index_min == index_max:
                parent_node.add_child(segment_tree_node(array[index_min] ,index_min, index_max, node_parent))
            else:
                difference_min_max = (index_max - index_min) // 2
                new_node = segment_tree_node(sum(array[index_min:index_max+1]), index_min, index_max, node_parent)
                parent_node.add_child(new_node)
                node_to_create.append((new_node, index_min + difference_min_max+1, index_max))
                node_to_create.append((new_node, index_min, index_min + difference_min_max))

    # this is an AI generated function that prints the tree in a neat way in the terminal.
    def print_tree(self):
        def print_(node, prefix="", is_left=False):
            if node is None:
                return
            connector = "├── " if is_left else "└── "
            range_str = f"[{node.index_min}..{node.index_max}]"
            print(prefix + connector + f"{range_str} val={node.value}")

            child_prefix = prefix + ("│   " if is_left else "    ")
            print_(node.left, child_prefix, is_left=True)
            print_(node.right, child_prefix, is_left=False)
        print_(self.root)

    def query(self, l, r, node = None):
        if node is None:
            node = self.root

        if node.index_max < l or node.index_min > r:
            return 0

        if l <= node.index_min and node.index_max <= r:
            return node.value

        return self.query(l, r, node.left) + self.query(l, r, node.right)

    def get_range_max(self,l,r):
        node = self.root
        maximum = 0
        node_to_explore = [node.left,node.right]
        while node_to_explore:
            node = node_to_explore.pop(0)
            if node.index_max == node.index_min and node.index_max <= r and node.index_min >= l:
                if node.value > maximum:
                    maximum = node.value
            elif l <= node.index_max and node.index_min <= r:
                node_to_explore.append(node.left)
                node_to_explore.append(node.right)
        return maximum

    def get_range_min(self,l,r):
        node = self.root
        minimum = inf
        node_to_explore = [node.left,node.right]
        while node_to_explore:
            node = node_to_explore.pop(0)
            if node.index_max == node.index_min and node.index_max <= r and node.index_min >= l:
                if node.value < minimum:
                    minimum = node.value
            elif l <= node.index_max and node.index_min <= r:
                node_to_explore.append(node.left)
                node_to_explore.append(node.right)
        return minimum

    def get_tree_size(self):
        nbNodes = 1
        node = self.root
        node_to_explore = [node.left,node.right]
        while node_to_explore:
            node = node_to_explore.pop(0)
            nbNodes += 1
            if not node.index_max == node.index_min:
                node_to_explore.append(node.left)
                node_to_explore.append(node.right)
        return nbNodes

    def get_height(self):
        height_max = 0
        node = self.root
        node_to_explore = [(node.left,1),(node.right,1)]
        while node_to_explore:
            node, height = node_to_explore.pop(0)
            if node.index_max == node.index_min:
                if height > height_max:
                    height_max = height
            else:
                node_to_explore.append((node.left,height+1))
                node_to_explore.append((node.right,height+1))
        return height_max

    def get_leaf_values(self):
        node = self.root
        leaf_nodes = []
        node_to_visit = [node.right,node.left]
        while node_to_visit:
            node = node_to_visit.pop(-1)
            if node.index_max == node.index_min:
                leaf_nodes.append(node.value)
            else:
                node_to_visit.append(node.right)
                node_to_visit.append(node.left)
        return leaf_nodes




def create_activity_array( days, max_posts):
    array = []
    for i in range(days):
        array.append(random.randint(1,max_posts))
    return array

print("\n---------- Part A: Trie for autocomplete ----------\n")
user1 = user("user1")
user2 = user("user2")
user3 = user("user3")
michel = user("michel")
mark = user("mark")
marguerite = user("marguerite")
ursula = user("ursula")
ursul = user("ursul")



trie = trie()
trie.insert(user1)
trie.insert(user2)
trie.insert(user3)
trie.insert(michel)
trie.insert(mark)
trie.insert(marguerite)
trie.insert(ursula)
trie.insert(ursul)

print("the trie:")
trie.print_trie()

print("trie search for mark: ", trie.search_trie("mark"))

print("start with function with ma: ", trie.start_with("ma"))
print("autocomplete function with ma: ", trie.autocomplete("ma"))
print("count words function: ", trie.count_words())
print("get height function: ", trie.get_height())
print("get total nodes function: ", trie.get_total_nodes())
trie.delete("michel")
print("Trie after michel deletion:")
trie.print_trie()

print("insertion of 50000 usernames")
for username in usernames:
    trie.insert(user(username))


print("autocomplete function with ammar: ", trie.autocomplete("ammar"))
print("count words function: ", trie.count_words())
print("get height function: ", trie.get_height())
print("get total nodes function: ", trie.get_total_nodes())


print("\n---------- Part B: Segment Tree for Activity Range Queries ----------\n")

test_array = create_activity_array(50,1000)
print(test_array)
segmented_tree = segment_tree()
segmented_tree.build(test_array)
segmented_tree.print_tree()

print("query for [43,50]: ",segmented_tree.query(43,50))
print("maximum for [11,14]: ",segmented_tree.get_range_max(11,14))
print("minimum for [11,14]: ",segmented_tree.get_range_min(11,14))
print("number of nodes in the tree: ", segmented_tree.get_tree_size())
print("height of the tree: ", segmented_tree.get_height())
print("leaves nodes: ", segmented_tree.get_leaf_values())
