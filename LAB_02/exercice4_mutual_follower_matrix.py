class SocialGroup:
    def __init__(self):
        self.matrix = []
        self.people_id = []
        self.size = 0

    def get_matrix(self):
        return self.matrix

    def follow(self, follower, followe):
        self.matrix[SocialGroup.get_id(self,follower)][SocialGroup.get_id(self,followe)] = True

    def UnFollow(self, i, j):
        self.matrix[i][j] = False

    def get_id(self, name):
        for i in range(self.size):
            if name == self.people_id[i]:
                return i

    def add_someone(self, name):
        self.people_id.append(name)
        for i in range(self.size):
            self.matrix[i].append(False)
        self.matrix.append([False]*len(self.people_id))
        self.size += 1

    def Is_following(self, i, j):
        return self.matrix[i][j]

    def get_follower(self,user):
        user_id = SocialGroup.get_id(self,user)
        followers = []
        for i in range(self.size):
            if self.matrix[i][user_id]:
                print(self.matrix[i][user_id])
                followers.append(self.people_id[i])
        return followers

    def get_following(self,user):
        user_id = SocialGroup.get_id(self,user)
        following = []
        for i in range(self.size):
            if self.matrix[user_id][i]:
                following.append(self.people_id[i])
        return following

    def get_mutual_follow(self):
        result = []
        for i in range(self.size):
            if self.matrix[i]:
                for j in range(i, self.size):
                    if self.matrix[i][j] and  self.matrix[j][i]:
                        result.append([self.people_id[i], self.people_id[j]])
        return result

    def influence_score(self, user):
        user_id = SocialGroup.get_id(self,user)
        score = 0
        for i in range(self.size):
            if i == user_id:
                for j in range(self.size):
                    if self.matrix[i][j]:
                        score += 1
            if self.matrix[i][user_id]:
                score += 1
        return score/self.size

group = SocialGroup()
group.add_someone("greg")
group.add_someone("louis")
group.follow("greg","louis")
group.add_someone("margarita")
group.add_someone("michel")
group.follow("louis","greg")
group.follow("louis","michel")
print(group.get_mutual_follow())
print(group.influence_score("louis"), group.influence_score("michel"))