class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class SocialGraph:
    def __init__(self, original_user):
        self.matrix = [[False]]
        self.user_in_matrix = [original_user]
        self.list = [Node(original_user)]

    def add_user(self, user):
        self.user_in_matrix.append(user)
        for i in range(len(self.matrix)):
            self.matrix[i].append(False)
        self.matrix.append([False for i in range(len(self.matrix)+1)])
        self.list.append(Node(user))

    def get_user_id(self, name):
        for i in range(len(self.user_in_matrix)):
            if self.user_in_matrix[i] == name:
                return i
        print("User not found")
        return None

    def add_friendship(self, user1, user2):
        user1_id = self.get_user_id(user1)
        user2_id = self.get_user_id(user2)
        self.matrix[user1_id][user2_id] = True
        node = self.list[user1_id]
        while node.next is not None:
            node = node.next
        node.next = Node(user2)

    def represent_list(self):
        result = ""
        for element in self.list:
            result += element.data.name + " follows : "
            while element.next is not None:
                result += element.next.data.name + ", "
                element = element.next
            result += "\n"
        return result

    def dfs_recursive(self,user, result = []):
        user_id = self.get_user_id(user)
        result.append(user)
        if user_id is None:
            return "user not found"
        for i in range(len(self.matrix)):
            if self.matrix[user_id][i]:
                curr_user = self.user_in_matrix[i]
                if not curr_user in result:
                    self.dfs_recursive(curr_user, result)
        return result

    def dfs_recursive_all(self,result = []):
        for user in self.user_in_matrix:
            if not user in result:
                self.dfs_recursive(user, result)

        for i in range(len(result)):
            result[i] = result[i].__str__()
        return result

    def dfs_iterative(self, user):
        result = []
        stack = [user]
        while stack:
            user = stack.pop()
            result.append(user)
            user_id = self.get_user_id(user)
            user_node = self.list[user_id]
            while user_node.next is not None:
                if not user_node.next.data in result:
                    stack.append(user_node.next.data)
                user_node = user_node.next

        return result

    def is_graph_connected(self):
        connections = self.find_all_connected()
        if len(connections) == 1:
            return True
        return False

    def does_path_exist(self, user1, user2):
        connections = self.find_all_connected()
        for connection in connections:
            if user1 in connection and user2 in connection:
                return True
        return False

    def find_path(self, user1, user2):
        connections = self.find_all_connected()
        result = []
        user_found = False
        for connection in connections:
            if user1 in connection and user2 in connection:
                for user in connection:
                    if user_found:
                        result.append(user)
                        if user == user1 or user == user2:
                            return result
                    if user == user1 or user == user2:
                        result.append(user)
                        user_found = True
        return "path not found"

   # I had struggle on how to find all connected component with a directed graph
    # thanks to this video : https://www.youtube.com/watch?v=AWuSQuv8EX0 I understood the code
    def find_all_connected(self):
        visited = []
        finish_stack = []

        def dfs_finish(user):
            visited.append(user)
            user_id = self.get_user_id(user)
            for i in range(len(self.matrix)):
                if self.matrix[user_id][i] and self.user_in_matrix[i] not in visited:
                    dfs_finish(self.user_in_matrix[i])
            finish_stack.append(user)

        for user in self.user_in_matrix:
            if user not in visited:
                dfs_finish(user)

        n = len(self.user_in_matrix)
        transposed = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                transposed[j][i] = self.matrix[i][j]
        visited2 = []

        def dfs_transposed(user, component):
            visited2.append(user)
            component.append(user)
            user_id = self.get_user_id(user)
            for i in range(n):
                if transposed[user_id][i] and self.user_in_matrix[i] not in visited2:
                    dfs_transposed(self.user_in_matrix[i], component)

        sccs = []
        while finish_stack:
            user = finish_stack.pop()
            if user not in visited2:
                component = []
                dfs_transposed(user, component)
                sccs.append(component)

        return sccs

    def get_connected_compents_size(self):
        connected = self.find_all_connected()
        result = []
        for component in connected:
            result.append(len(component))
        return result

    def find_largest_component(self):
        connected = self.find_all_connected()
        biggest = connected[0]
        for component in connected:
            if len(component) > len(biggest):
                biggest = component
        return biggest

    def find_isolated_users(self):
        isolated_users = []
        connected = self.find_all_connected()
        for component in connected:
            if len(component) == 1:
                isolated_users.append(component[0])
        return isolated_users

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data) + " next: " + str(self.next.data if self.next else None)



def represent_array_user(users):
    result = ""
    for user in users:
        result += user.name + ", "
    return result[:-2]

def represent_array_array_user(users):
    result = ""
    for user in users:
        result += "[" + represent_array_user(user) + "],"
    return result[:-1]













original_user = User("original_user")
user1 = User("user1")
user2 = User("user2")
user3 = User("user3")
user4 = User("user4")
graph = SocialGraph(original_user)
graph.add_user(user1)
graph.add_user(user2)
graph.add_user(user3)
graph.add_user(user4)

graph.add_friendship(original_user, user4)
graph.add_friendship(user4, user2)
graph.add_friendship(user2, original_user)
graph.add_friendship(user1, user3)
graph.add_friendship(user3, user1)
graph.add_friendship(original_user, user3)
print("\nmatrix: ",graph.matrix)

print("\n--- list representation ---\n")
print(graph.represent_list())
print("dfs result: ",graph.dfs_recursive_all())

print("\n--- dfs iterative ---\n")
print(represent_array_user(graph.dfs_iterative(original_user)))

print("\n--- find all connected ---\n")
print(represent_array_array_user(graph.find_all_connected()))
print("is graph connected: ",graph.is_graph_connected())

print("\n--- paths ---\n")
print("does path exist between original_user and user1: ", graph.does_path_exist(original_user, user1))
print("path between original_user and user2: ",represent_array_user(graph.find_path(original_user, user2)))

print("\n---- analytics ---\n")
print("length of connected component: ",graph.get_connected_compents_size())
print("biggest component: ",represent_array_user(graph.find_largest_component()))
print("isolated users: ",represent_array_user(graph.find_isolated_users()))