
from collections import defaultdict


class SocialGraph:
    def __init__(self, num_users: int):
        self.num_users = num_users
        self.num_edges = 0

        # Adjacency Matrix
        self.matrix = [[0] * num_users for _ in range(num_users)]

        # Adjacency List
        self.adj_list = defaultdict(set)
        for i in range(num_users):
            self.adj_list[i] = set()

 
    def add_friendship(self, u: int, v: int):
        if u == v:
            return
        if self.matrix[u][v] == 0:
            self.matrix[u][v] = 1
            self.matrix[v][u] = 1

            self.adj_list[u].add(v)
            self.adj_list[v].add(u)

            self.num_edges += 1

    def remove_friendship(self, u: int, v: int):
        if self.matrix[u][v] == 1:
            self.matrix[u][v] = 0
            self.matrix[v][u] = 0

            self.adj_list[u].discard(v)
            self.adj_list[v].discard(u)

            self.num_edges -= 1

    def are_friends_matrix(self, u: int, v: int) -> bool:
        return self.matrix[u][v] == 1

    def are_friends_list(self, u: int, v: int) -> bool:
        return v in self.adj_list[u]

    def get_friends_matrix(self, u: int):
        return [i for i in range(self.num_users) if self.matrix[u][i] == 1]

    def get_friends_list(self, u: int):
        return list(self.adj_list[u])

    def get_degree(self, u: int) -> int:
        return len(self.adj_list[u])

    def get_num_users(self) -> int:
        return self.num_users

    def get_num_edges(self) -> int:
        return self.num_edges

  
    def is_complete_graph(self) -> bool:
        for u in range(self.num_users):
            if self.get_degree(u) != self.num_users - 1:
                return False
        return True

    def graph_density(self) -> float:
        if self.num_users <= 1:
            return 0.0
        return (2 * self.num_edges) / (self.num_users * (self.num_users - 1))

    def degree_distribution(self):
        distribution = {}
        for u in range(self.num_users):
            degree = self.get_degree(u)
            distribution[degree] = distribution.get(degree, 0) + 1
        return distribution

   
    def matrix_to_list(self):
        converted = defaultdict(list)
        for i in range(self.num_users):
            for j in range(self.num_users):
                if self.matrix[i][j] == 1:
                    converted[i].append(j)
        return dict(converted)

    def list_to_matrix(self):
        converted = [[0] * self.num_users for _ in range(self.num_users)]
        for u in self.adj_list:
            for v in self.adj_list[u]:
                converted[u][v] = 1
        return converted



if __name__ == "__main__":
    graph = SocialGraph(5)

    graph.add_friendship(0, 1)
    graph.add_friendship(0, 2)
    graph.add_friendship(1, 2)
    graph.add_friendship(3, 4)

    print("Friends of 0 (list):", graph.get_friends_list(0))
    print("Friends of 0 (matrix):", graph.get_friends_matrix(0))
    print("Are 0 and 1 friends?", graph.are_friends_list(0, 1))
    print("Degree of 0:", graph.get_degree(0))
    print("Total users:", graph.get_num_users())
    print("Total edges:", graph.get_num_edges())
    print("Density:", graph.graph_density())
    print("Degree distribution:", graph.degree_distribution())
    print("Is complete graph?", graph.is_complete_graph())
    print("Matrix to list:", graph.matrix_to_list())
