from collections import deque

class SocialNetwork:
    def __init__(self):
        self.adjacency_list = {}

    def add_user(self,user):
        if user not in self.adjacency_list:
            self.adjacency_list[user] = []
    
    def add_friendship(self,user1,user2):
        if user1 in self.adjacency_list and user2 in self.adjacency_list:
            if user2 not in self.adjacency_list[user1]:
                self.adjacency_list[user1].append(user2)
            if user1 not in self.adjacency_list[user2]:
                self.adjacency_list[user2].append(user1)

    def bfs(self,start_user):
        order = []
        visited = set()
        queue = deque()

        visited.add(start_user)
        queue.append(start_user)

        while queue:
            user = queue.popleft()
            order.append(user)
            for neighbor in self.adjacency_list[user]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
            
        return order
    

    def bfs_with_distances(self,start_user):
        queue = deque()
        distances = {start_user:0}
        queue.append(start_user)

        while queue:
            user = queue.popleft()

            for neighbor in self.adjacency_list[user]:
                if neighbor not in distances:
                    distances[neighbor] = distances[user] + 1
                    queue.append(neighbor)
        
        return distances
    

    def shortest_path(self,start_user,target_user):
        if start_user == target_user:
            return [start_user]
        
        parent = {start_user:None}
        queue = [start_user]

        while queue:
            user = queue.pop(0)
            for neighbor in self.adjacency_list[user]:
                if neighbor not in parent:
                    parent[neighbor] = user

                    if neighbor == target_user:
                        path = []
                        curr = target_user
                        while curr is not None:
                            path.append(curr)
                            curr = parent[curr]
                        path.reverse()
                        return path
                    queue.append(neighbor)
            
        return None
    
    def degrees_of_separation(self, start_user, target_user):
        distances = self.bfs_with_distances(start_user)
        return distances.get(target_user, -1)
    

    def friends_within_k_hops(self, start_user, k):
        distances = self.bfs_with_distances(start_user)
        result = set()
    
        for user, distance in distances.items():
            if 1 <= distance <= k:
                result.add(user)
        
        return result
    


    def compute_average_degrees_of_separation(self):
        total_distance = 0
        count = 0
        users = list(self.adjacency_list.keys())
        n = len(users)

        for i in range(n):
            user = users[i]
            distances = self.bfs_with_distances(user)

            for j in range(i+1,n):
                target = users[j]
                dist = distances.get(target,None)
                if dist is not None:
                    total_distance = total_distance + dist
                    count = count + 1
        if count == 0:
            return 0
        
        return total_distance / count
    

    
    def get_distance_distribution(self, start_user):
        distances = self.bfs_with_distances(start_user)
        distribution = {}
    
        for user, dist in distances.items():
            if user != start_user:
                distribution[dist] = distribution.get(dist, 0) + 1
    
        return distribution


    def recommend_friends(self, start_user, max_recommendations=5):
        distances = self.bfs_with_distances(start_user)
        current_friends = set(self.adjacency_list[start_user])
        candidates = {}
    
        for user, dist in distances.items():
            if dist == 2 and user not in current_friends and user != start_user:
                user_friends = set(self.adjacency_list[user])
                common_friends = user_friends.intersection(current_friends)
                count = len(common_friends)
                candidates[user] = count
    
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
    
        result = [user for user, count in sorted_candidates[:max_recommendations]]
    
        return result
    


    # TEST CASES


sn = SocialNetwork()

# Add users
sn.add_user("Alice")
sn.add_user("Bob")
sn.add_user("Charlie")
sn.add_user("David")
sn.add_user("Eve")
sn.add_user("Frank")
sn.add_user("Grace")

# add friendships
sn.add_friendship("Alice", "Bob")
sn.add_friendship("Alice", "Charlie")
sn.add_friendship("Bob", "David")
sn.add_friendship("Charlie", "David")
sn.add_friendship("David", "Eve")
sn.add_friendship("Eve", "Frank")
sn.add_friendship("Frank", "Grace")

# test add_user  add_friendship
print("=== test structure ===")
print(sn.adjacency_list)

# test bfs
print("\n=== test bfs ===")
print(sn.bfs("Alice"))

print("\n=== test bfs_with_distances ===")
print(sn.bfs_with_distances("Alice"))

# test shortest_path
print("\n=== test shortest_path ===")
print(sn.shortest_path("Alice", "Eve"))
print(sn.shortest_path("Alice", "Grace"))
print(sn.shortest_path("Alice", "Alice"))

# test degrees_of_separation
print("\n=== test degrees_of_separation ===")
print(sn.degrees_of_separation("Alice", "Eve"))
print(sn.degrees_of_separation("Alice", "Grace"))
print(sn.degrees_of_separation("Alice", "NotFound"))

# test friends_within_k_hops
print("\n=== test friends_within_k_hops ===")
print(sn.friends_within_k_hops("Alice", 1))
print(sn.friends_within_k_hops("Alice", 2))
print(sn.friends_within_k_hops("Alice", 3))

# test compute_average_degrees_of_separation
print("\n=== test compute_average_degrees_of_separation ===")
print(sn.compute_average_degrees_of_separation())

# test get_distance_distribution
print("\n=== test get_distance_distribution ===")
print(sn.get_distance_distribution("Alice"))

# test recommend_friends
print("\n=== test recommend_friends ===")
print(sn.recommend_friends("Alice", 5))

# single user network
print("\n=== test single user network ===")
sn2 = SocialNetwork()
sn2.add_user("Solo")
print(sn2.bfs("Solo"))
print(sn2.bfs_with_distances("Solo"))
print(sn2.shortest_path("Solo", "Solo"))
print(sn2.degrees_of_separation("Solo", "Solo"))
print(sn2.friends_within_k_hops("Solo", 1))
print(sn2.compute_average_degrees_of_separation())
print(sn2.get_distance_distribution("Solo"))
print(sn2.recommend_friends("Solo"))

# No network connection
print("\n===  test No network connection ===")
sn3 = SocialNetwork()
sn3.add_user("User1")
sn3.add_user("User2")
sn3.add_user("User3")
print(sn3.shortest_path("User1", "User2"))
print(sn3.degrees_of_separation("User1", "User2"))
print(sn3.compute_average_degrees_of_separation())