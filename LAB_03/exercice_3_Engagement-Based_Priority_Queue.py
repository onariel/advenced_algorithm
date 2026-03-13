from datetime import datetime,timedelta
import math

class Post:
    def __init__(self,post_id:str,user_id:str,content:str,timestamp:datetime,likes:int=0,
                 comments:int = 0,shares:int = 0):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.comments = comments
        self.shares = shares

    def engagement_score(self) ->int:
        return (self.likes * 1) + (self.comments * 2) + (self.shares * 3)

#2 Define nodes
class QueueNode:
    def __init__(self,data:Post):
        self.val = data
        self.link = None

#3. Class PriorityQueue and operations
class PriorityQueue:
    def __init__(self):
        self.head = None
        self.rear = None
        self.count = 0
    def is_empty(self) -> bool:
        return self.head is None
    def size(self) -> int:
        return self.count
    def peek_max(self) -> Post | None:
        if self.head is not None:
            return self.head.val
        else:
            return None

    def enqueue(self, post: Post):
        new_node = QueueNode(post)
        if self.head is None:
            self.head = new_node
            self.rear = new_node
        elif new_node.val.engagement_score() > self.head.val.engagement_score():
            new_node.link = self.head
            self.head = new_node
        else:
            current = self.head
            while current.link is not None and current.link.val.engagement_score() >= new_node.val.engagement_score():
                current = current.link
            new_node.link = current.link
            current.link = new_node
            if new_node.link is None:
                self.rear = new_node
        
        self.count += 1

    def dequeue_max(self) -> Post | None:
        if self.is_empty():
            print("error. Queue is empty")
            return None
        
        to_delete = self.head
        max_post = to_delete.val  
        
        if self.head.link is None:
            self.head = None
            self.rear = None
        else:
            self.head = self.head.link
        
        del to_delete
        self.count -= 1
        return max_post


# 4. Priority updates: 
    def update_score(self, post_id: str, new_likes: int, new_comments: int, new_shares: int):
        prev = None
        current = self.head
        target_node = None

        while current is not None:
            if current.val.post_id == post_id:
                target_node = current
                if prev is None:
                    self.head = current.link
                else:  
                    prev.link = current.link
                if current == self.rear:
                    self.rear = prev
                self.count -= 1
                break  
            prev = current
            current = current.link
        if target_node is not None:
            target_node.val.likes = new_likes
            target_node.val.comments = new_comments
            target_node.val.shares = new_shares
            self.enqueue(target_node.val)


    def refresh_all(self):
        temp_list = []
        current = self.head
        while current is not None:
            temp_list.append(current.val)
            current = current.link
        self.head = None
        self.rear = None
        self.count = 0
        for post in temp_list:
            self.enqueue(post)

#5.Trending window: 
    def get_top_k(self, k: int) -> list[Post]:
        result = []
        current = self.head
        count = 0
        while current is not None and count < k:
            result.append(current.val)
            current = current.link
            count += 1
        return result

    def decay_older_than(self, cutoff_time: datetime, decay_rate: float = 0.2):
        temp_list = []
        current = self.head
        while current is not None:
            post = current.val
            if post.timestamp < cutoff_time:
                original_score = post.engagement_score()
                decayed_score = math.floor(original_score * (1 - decay_rate))
                scale = decayed_score / original_score if original_score != 0 else 1.0
                post.likes = math.floor(post.likes * scale)
                post.comments = math.floor(post.comments * scale)
                post.shares = math.floor(post.shares * scale)
            temp_list.append(post)
            current = current.link
        self.head = None
        self.rear = None
        self.count = 0
        for post in temp_list:
            self.enqueue(post)






#TESTS
if __name__ == "__main__":
    print("="*50)
    print("TESTS PriorityQueue")
    print("="*50)
    
    now = datetime.now()
    
    # Post3: score 95, Post1: score 82, Post2: score 47, Post4: score 23
    post1 = Post("Post1", "u1", "帖子1", now - timedelta(minutes=30), likes=82, comments=0, shares=0)  # 82分
    post2 = Post("Post2", "u2", "帖子2", now - timedelta(minutes=45), likes=47, comments=0, shares=0)  # 47分
    post3 = Post("Post3", "u3", "帖子3", now - timedelta(hours=2), likes=95, comments=0, shares=0)     # 95分（旧帖子）
    post4 = Post("Post4", "u4", "帖子4", now - timedelta(hours=3), likes=23, comments=0, shares=0)     # 23分（旧帖子）
    
    print("\n1. Initial queue:")
    pq = PriorityQueue()
    pq.enqueue(post3)
    pq.enqueue(post1)
    pq.enqueue(post2)
    pq.enqueue(post4)
    

    current = pq.head
    queue_str = []
    while current:
        queue_str.append(f"{current.val.post_id}:{current.val.engagement_score()}")
        current = current.link
    print("  Initial queue:", " -> ".join(queue_str))
    print("  [Post3:95] -> [Post1:82] -> [Post2:47] -> [Post4:23]")
    
    print("\n2. Post 2 received 10 likes.:")
    current = pq.head
    while current:
        if current.val.post_id == "Post2":
            print(f"  Before update {current.val.post_id} Score: {current.val.engagement_score()}")
        current = current.link
    
    pq.update_score("Post2", new_likes=57, new_comments=0, new_shares=0)  
    
    current = pq.head
    queue_str = []
    while current:
        queue_str.append(f"{current.val.post_id}:{current.val.engagement_score()}")
        current = current.link
    print("  After update:", " -> ".join(queue_str))
    print("  [Post3:95] -> [Post1:82] -> [Post2:57] -> [Post4:23]")
    
    print("\n3. Reduce by 20% if it lasts more than 1 hour:")
    cutoff = now - timedelta(hours=1)
    pq.decay_older_than(cutoff, decay_rate=0.2)
    
    current = pq.head
    queue_str = []
    scores = {}
    while current:
        queue_str.append(f"{current.val.post_id}:{current.val.engagement_score()}")
        scores[current.val.post_id] = current.val.engagement_score()
        current = current.link
    print("  queue:", " -> ".join(queue_str))
    print("   [Post1:82] -> [Post3:76] -> [Post2:57] -> [Post4:23]")
    
    print("\n4. results:")
    expected_order = ["Post1", "Post3", "Post2", "Post4"]
    current = pq.head
    correct = True
    for expected_id in expected_order:
        if current is None or current.val.post_id != expected_id:
            correct = False
            break
        current = current.link
    
    if correct and current is None:
        print("  ✅ yes test ok!")
    else:
        print("  ❌ error")
    
    print("\n5. Final score:")
    current = pq.head
    while current:
        post = current.val
        print(f"  {post.post_id}: likes={post.likes}, comments={post.comments}, "
              f"shares={post.shares}, engagement_score={post.engagement_score()}")
        current = current.link
    
    print("test finished!")