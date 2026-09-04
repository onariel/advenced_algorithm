class UserNode:
    def __init__(self, user_id, name, friends):
        self.user_id = user_id
        self.name = name
        self.friends = friends  
        self.left = None
        self.right = None

class UserBST:
    def __init__(self):
        self.root = None

    def insert(self, user_id, name, friends):
        self.root = self._insert(self.root, user_id, name, friends)

    def _insert(self, node, user_id, name, friends):
        if node is None:
            return UserNode(user_id, name, friends)

        if user_id < node.user_id:
            node.left = self._insert(node.left, user_id, name, friends)
        elif user_id > node.user_id:
            node.right = self._insert(node.right, user_id, name, friends)

        return node

    def find(self, user_id):
        return self._find(self.root, user_id)

    def _find(self, node, user_id):
        if node is None:
            return None

        if user_id == node.user_id:
            return node

        if user_id < node.user_id:
            return self._find(node.left, user_id)
        else:
            return self._find(node.right, user_id)

  
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.user_id)
            self._inorder(node.right, result)

  
    def delete(self, user_id):
        self.root = self._delete(self.root, user_id)

    def _delete(self, node, user_id):
        if node is None:
            return None

        if user_id < node.user_id:
            node.left = self._delete(node.left, user_id)

        elif user_id > node.user_id:
            node.right = self._delete(node.right, user_id)

        else:
         
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left


            successor = self._min(node.right)
            node.user_id = successor.user_id
            node.name = successor.name
            node.friends = successor.friends
            node.right = self._delete(node.right, successor.user_id)

        return node

    def _min(self, node):
        while node.left:
            node = node.left
        return node


    def suggest_friends(self, user_id, max_suggestions=5):
        user = self.find(user_id)
        if user is None:
            return []

        count = {}
        direct = set(user.friends)

        for f in direct:
            friend_node = self.find(f)
            if friend_node is None:
                continue

            for fof in friend_node.friends:
                if fof != user_id and fof not in direct:
                    count[fof] = count.get(fof, 0) + 1


        sorted_users = sorted(count.items(), key=lambda x: x[1], reverse=True)

        return [uid for uid, _ in sorted_users[:max_suggestions]]


    def get_height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))


    def is_balanced(self):
        return self._is_balanced(self.root)

    def _is_balanced(self, node):
        if node is None:
            return True

        left = self._height(node.left)
        right = self._height(node.right)

        if abs(left - right) > 1:
            return False

        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def get_leaf_count(self):
        return self._leaf_count(self.root)

    def _leaf_count(self, node):
        if node is None:
            return 0

        if node.left is None and node.right is None:
            return 1

        return self._leaf_count(node.left) + self._leaf_count(node.right)
