import math

# Cosine Similarity Function

def cosine_similarity(user_a, user_b):
    dot = 0
    
    norm_a = 0
    norm_b = 0
    
    for i in range(len(user_a)):
        dot += user_a[i] * user_b[i]
        norm_a += user_a[i] ** 2
        norm_b += user_b[i] ** 2
    
    if norm_a == 0 or norm_b == 0:
        return 0
    
    similarity = dot / (math.sqrt(norm_a) * math.sqrt(norm_b))
    return similarity


print("Similarity User0 & User1:", round(cosine_similarity(user_interest[0], user_interest[1]), 2))
print("Similarity User0 & User2:", round(cosine_similarity(user_interest[0], user_interest[2]), 2))


# Top K Similar Users

def top_k_similar_users(target_user_id, K):
    similarities = []
    target_vector = user_interest[target_user_id]
    
    for uid in range(len(user_interest)):
        if uid != target_user_id and uid not in friends.get(target_user_id, set()):
            sim = cosine_similarity(target_vector, user_interest[uid])
            similarities.append((uid, sim))
    
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
   
    return similarities[:K]

print("Top 2 similar users to User 0:", top_k_similar_users(0, 2))


# Recommend Interests

def recommend_interests(target_user_id, K=2, top_n=3):
    similar_users = top_k_similar_users(target_user_id, K)
    target_vector = user_interest[target_user_id]
    
    scores = {}
    
    for i in range(len(target_vector)):
        if target_vector[i] == 0:  
            score = 0
            for uid, sim in similar_users:
                score += sim * user_interest[uid][i]
            scores[i] = score
    

    recommended = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
 
    result = []
    for i, score in recommended[:top_n]:
        result.append((interests[i], round(score, 2)))
    
    return result

print("Recommended interests for User 0:", recommend_interests(0, K=2, top_n=3))



interests = ["Music", "Sports", "Tech", "Fashion", "Travel", "Food"]
print(interests)

user_interest = [
    [10, 0, 8, 2, 5, 7],  
    [9, 1, 7, 3, 6, 8],   
    [2, 9, 1, 8, 3, 0],   
    [0, 5, 0, 7, 1, 2]    
]
print(user_interest)

friends = {0: {3}, 1: set(), 2: set(), 3: {0}}


