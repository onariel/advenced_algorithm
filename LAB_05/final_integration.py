"""
LAB 4 – Final Integration
Feature: "Engagement Analytics with Nested Comments"

Combines:
  - Set operations          → users who commented on multiple posts
  - Doubly linked list      → navigate top posts (adapted from LAB 2 feed)
  - Priority queue (heap)   → rank posts by engagement score
  - Recursive algorithms    → process nested comment threads (LAB 4 Ex 1–3)
"""

import datetime
import random
import heapq
from collections import deque


# ──────────────────────────────────────────────────────────────
# 1.  DATA STRUCTURES
# ──────────────────────────────────────────────────────────────

class CommentNode:
    """Nested comment node (Exercise 1)."""

    def __init__(self, comment_id, user_id, content, timestamp=None, likes=0):
        self.comment_id = comment_id
        self.user_id = user_id
        self.content = content[:100]
        self.timestamp = timestamp or datetime.datetime.now()
        self.likes = likes
        self.replies: list["CommentNode"] = []

    def add_reply(self, reply: "CommentNode"):
        self.replies.append(reply)

    def __repr__(self):
        return f"Comment({self.comment_id}, user={self.user_id}, likes={self.likes})"


class Post:
    """Post with engagement score and nested comment thread."""

    def __init__(self, post_id, user_id, content_preview, likes=0, comments_count=0, shares=0):
        self.post_id = post_id
        self.user_id = user_id
        self.content_preview = content_preview
        self.timestamp = datetime.datetime.now()
        self.likes = likes
        self.comments_count = comments_count
        self.shares = shares
        self.comment_thread: list[CommentNode] = []   # top-level comments

    @property
    def engagement_score(self):
        return self.likes * 1 + self.comments_count * 2 + self.shares * 3

    # make Post comparable for the heap (max-heap via negation)
    def __lt__(self, other):
        return self.engagement_score > other.engagement_score

    def __repr__(self):
        return (f"Post({self.post_id}, user={self.user_id}, "
                f"engagement={self.engagement_score})")


# ── Doubly-linked list node (adapted from LAB 2) ──────────────

class PostNode:
    """Node in the doubly-linked list of top posts."""

    def __init__(self, post: Post):
        self.post = post
        self.next: "PostNode | None" = None
        self.prev: "PostNode | None" = None

    def __repr__(self):
        return f"PostNode({self.post})"


class TopPostsFeed:
    """
    Doubly-linked list that stores posts ordered by engagement score.
    Supports forward / backward navigation (same interface as LAB 2 feed).
    """

    def __init__(self):
        self.head: PostNode | None = None
        self.tail: PostNode | None = None
        self.current: PostNode | None = None
        self.size = 0

    # -- build / mutate ----------------------------------------

    def insert_sorted(self, post: Post):
        """Insert post in descending engagement-score order.  O(n)"""
        new_node = PostNode(post)
        self.size += 1

        if self.head is None:
            self.head = self.tail = self.current = new_node
            return

        # find insertion position
        pointer = self.head
        while pointer and pointer.post.engagement_score >= post.engagement_score:
            pointer = pointer.next

        if pointer is None:
            # append at tail
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        elif pointer is self.head:
            # prepend
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            self.current = self.head
        else:
            # middle
            new_node.prev = pointer.prev
            new_node.next = pointer
            pointer.prev.next = new_node
            pointer.prev = new_node

    # -- navigation --------------------------------------------

    def move_forward(self):
        if self.current is None or self.current.next is None:
            return "Already at last post."
        self.current = self.current.next
        return self.current.post

    def move_backward(self):
        if self.current is None or self.current.prev is None:
            return "Already at first post."
        self.current = self.current.prev
        return self.current.post

    def reset_to_top(self):
        self.current = self.head

    def display(self):
        result, node = [], self.head
        while node:
            marker = " ← current" if node is self.current else ""
            result.append(f"  {node.post}{marker}")
            node = node.next
        return "\n".join(result)


# ──────────────────────────────────────────────────────────────
# 2.  RECURSIVE ALGORITHMS  (Exercise 1 & 2 helpers)
# ──────────────────────────────────────────────────────────────

def collect_user_ids_recursive(comment: CommentNode, result: set) -> set:
    """
    Recursively collect every user_id that appears in a comment thread.
    Uses DFS – depth-first via the call stack.
    Time: O(n)  where n = total comments in thread.
    """
    result.add(comment.user_id)
    for reply in comment.replies:
        collect_user_ids_recursive(reply, result)
    return result


def count_total_comments(comment: CommentNode) -> int:
    """Recursively count all comments (including nested). O(n)"""
    return 1 + sum(count_total_comments(r) for r in comment.replies)


def total_likes(comment: CommentNode) -> int:
    """Recursively sum likes across an entire thread. O(n)"""
    return comment.likes + sum(total_likes(r) for r in comment.replies)


def find_deepest_reply(comment: CommentNode, depth: int = 0) -> int:
    """Recursively find maximum nesting depth. O(n)"""
    if not comment.replies:
        return depth
    return max(find_deepest_reply(r, depth + 1) for r in comment.replies)


def display_thread(comment: CommentNode, level: int = 0):
    """Recursively display thread with indentation."""
    indent = "  " * level
    print(f"{indent}[{comment.comment_id}] user={comment.user_id} "
          f"| likes={comment.likes} | \"{comment.content}\"")
    for reply in comment.replies:
        display_thread(reply, level + 1)


# ── Divide & Conquer (Exercise 2) ─────────────────────────────

def max_engagement(posts: list[Post], left: int, right: int) -> Post:
    """Recursively find post with highest engagement score. O(n)"""
    if left == right:
        return posts[left]
    mid = (left + right) // 2
    left_max = max_engagement(posts, left, mid)
    right_max = max_engagement(posts, mid + 1, right)
    return left_max if left_max.engagement_score >= right_max.engagement_score else right_max


def sum_engagement(posts: list[Post], left: int, right: int) -> int:
    """Recursively sum engagement scores. O(n)"""
    if left == right:
        return posts[left].engagement_score
    mid = (left + right) // 2
    return sum_engagement(posts, left, mid) + sum_engagement(posts, mid + 1, right)


# ──────────────────────────────────────────────────────────────
# 3.  ITERATIVE FALLBACK  (Exercise 3 – stack overflow protection)
# ──────────────────────────────────────────────────────────────

MAX_SAFE_DEPTH = 500   # Python default recursion limit ~1000

def collect_user_ids_iterative(comment: CommentNode) -> set:
    """
    Iterative DFS with explicit stack – safe for arbitrarily deep threads.
    Produces the same result as collect_user_ids_recursive.
    """
    user_ids = set()
    stack = [comment]
    while stack:
        node = stack.pop()
        user_ids.add(node.user_id)
        # push replies in reverse so left-most is processed first
        for reply in reversed(node.replies):
            stack.append(reply)
    return user_ids


def flatten_iterative(comment: CommentNode) -> list[CommentNode]:
    """Depth-first flattening without recursion (Exercise 3)."""
    result, stack = [], [comment]
    while stack:
        node = stack.pop()
        result.append(node)
        for reply in reversed(node.replies):
            stack.append(reply)
    return result


def collect_user_ids_safe(comment: CommentNode, depth: int = 0) -> set:
    """
    Dispatcher: uses recursion for shallow threads, iterative for deep ones.
    This is the production-safe version.
    """
    if depth > MAX_SAFE_DEPTH or find_deepest_reply(comment) > MAX_SAFE_DEPTH:
        return collect_user_ids_iterative(comment)
    return collect_user_ids_recursive(comment, set())


# ──────────────────────────────────────────────────────────────
# 4.  SET OPERATIONS  – cross-post user analytics
# ──────────────────────────────────────────────────────────────

def users_per_post(post: Post) -> set:
    """
    Return the set of user_ids that commented on a post
    (across the entire nested thread).
    Uses the safe dispatcher above.
    """
    user_ids = set()
    for top_comment in post.comment_thread:
        user_ids |= collect_user_ids_safe(top_comment)
    return user_ids


def users_on_multiple_posts(posts: list[Post]) -> dict[int, set]:
    """
    Set intersection analytics:
      - For every pair of posts, find users who commented on BOTH.
    Returns a dict keyed by (post_id_a, post_id_b) → common user_ids.
    O(P² × n) where P = number of posts, n = comments per post.
    """
    per_post = {p.post_id: users_per_post(p) for p in posts}
    cross = {}
    post_ids = list(per_post.keys())
    for i in range(len(post_ids)):
        for j in range(i + 1, len(post_ids)):
            a, b = post_ids[i], post_ids[j]
            common = per_post[a] & per_post[b]
            if common:
                cross[(a, b)] = common
    return cross


def most_active_users(posts: list[Post], top_k: int = 5) -> list[tuple]:
    """
    Count how many distinct posts each user commented on.
    Uses set union across posts.  Returns top_k users.
    """
    activity: dict[int, int] = {}
    for post in posts:
        for uid in users_per_post(post):
            activity[uid] = activity.get(uid, 0) + 1
    # use a min-heap of size k to get top-k  (iterative, O(n log k))
    heap = []
    for uid, count in activity.items():
        heapq.heappush(heap, (count, uid))
        if len(heap) > top_k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)   # [(count, user_id), ...]


# ──────────────────────────────────────────────────────────────
# 5.  PRIORITY QUEUE  – rank posts by engagement
# ──────────────────────────────────────────────────────────────

class EngagementPriorityQueue:
    """
    Max-heap of posts ranked by engagement_score.
    Python's heapq is a min-heap, so we negate the score.
    """

    def __init__(self):
        self._heap: list[tuple] = []   # (neg_score, post_id, Post)
        self._counter = 0              # tie-breaker

    def push(self, post: Post):
        heapq.heappush(self._heap, (-post.engagement_score, self._counter, post))
        self._counter += 1

    def pop(self) -> Post | None:
        if not self._heap:
            return None
        _, _, post = heapq.heappop(self._heap)
        return post

    def peek(self) -> Post | None:
        if not self._heap:
            return None
        return self._heap[0][2]

    def __len__(self):
        return len(self._heap)

    def top_k(self, k: int) -> list[Post]:
        """Return top-k posts without destroying the heap. O(k log n)"""
        result, temp = [], []
        for _ in range(min(k, len(self._heap))):
            post = self.pop()
            result.append(post)
            temp.append(post)
        for post in temp:          # restore
            self.push(post)
        return result


# ──────────────────────────────────────────────────────────────
# 6.  ENGAGEMENT ANALYTICS ENGINE  – the integration class
# ──────────────────────────────────────────────────────────────

class EngagementAnalytics:
    """
    Combines all four structures into a coherent analytics engine.

    Internal layout
    ───────────────
    _pq          : EngagementPriorityQueue   → always holds the full post set
    _top_feed    : TopPostsFeed              → doubly-linked list of top-N posts
                                               built from the priority queue
    _posts       : list[Post]               → master list (for D&C algorithms)
    """

    def __init__(self, top_n: int = 10):
        self._pq = EngagementPriorityQueue()
        self._top_feed = TopPostsFeed()
        self._posts: list[Post] = []
        self._top_n = top_n

    # -- ingestion ---------------------------------------------

    def add_post(self, post: Post):
        """
        Register a new post.
        - Push into priority queue           (O log n)
        - Insert into sorted doubly-linked list (O n)
        """
        self._posts.append(post)
        self._pq.push(post)
        self._top_feed.insert_sorted(post)

    # -- navigation (doubly-linked list) -----------------------

    def browse_next_top_post(self):
        return self._top_feed.move_forward()

    def browse_prev_top_post(self):
        return self._top_feed.move_backward()

    def reset_browsing(self):
        self._top_feed.reset_to_top()

    def show_feed(self):
        print("\n── Top Posts Feed (doubly-linked list) ──")
        print(self._top_feed.display())

    # -- priority queue queries --------------------------------

    def top_posts(self, k: int = 5) -> list[Post]:
        """Return k highest-engagement posts. O(k log n)"""
        return self._pq.top_k(k)

    # -- recursive thread analytics ----------------------------

    def thread_stats(self, post: Post) -> dict:
        """
        Recursively compute stats for all top-level comment threads of a post.
        Falls back to iterative if any thread is very deep.
        """
        total_comments = 0
        total_lks = 0
        max_depth = 0
        all_users: set = set()

        for top_comment in post.comment_thread:
            depth = find_deepest_reply(top_comment)

            if depth > MAX_SAFE_DEPTH:
                # Exercise 3 fallback: iterative flattening
                flat = flatten_iterative(top_comment)
                total_comments += len(flat)
                total_lks += sum(c.likes for c in flat)
                all_users |= {c.user_id for c in flat}
            else:
                # Exercise 1 recursive functions
                total_comments += count_total_comments(top_comment)
                total_lks += total_likes(top_comment)
                all_users |= collect_user_ids_recursive(top_comment, set())

            max_depth = max(max_depth, depth)

        return {
            "post_id": post.post_id,
            "total_comments": total_comments,
            "total_likes_in_threads": total_lks,
            "unique_commenters": len(all_users),
            "max_thread_depth": max_depth,
        }

    # -- set-operation analytics -------------------------------

    def cross_post_audience(self) -> dict:
        """Users who commented on more than one post (set intersection)."""
        return users_on_multiple_posts(self._posts)

    def top_active_users(self, k: int = 5) -> list[tuple]:
        """k users present on the most distinct posts."""
        return most_active_users(self._posts, k)

    # -- divide & conquer analytics ----------------------------

    def global_max_engagement(self) -> Post | None:
        if not self._posts:
            return None
        return max_engagement(self._posts, 0, len(self._posts) - 1)

    def global_avg_engagement(self) -> float:
        if not self._posts:
            return 0.0
        total = sum_engagement(self._posts, 0, len(self._posts) - 1)
        return total / len(self._posts)


# ──────────────────────────────────────────────────────────────
# 7.  DEMO
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ---------- build comment threads -------------------------
    # Structure from Exercise 1:
    # Comment 101 (Alice): "This recipe looks amazing!"
    #   ├── Reply 201 (Bob): "I tried it last night!"
    #   │   └── Reply 301 (Alice): "What did you think?"
    #   │       └── Reply 401 (Bob): "It was delicious!"
    #   └── Reply 202 (Charlie): "Can I use olive oil instead?"
    #       └── Reply 302 (Alice): "Yes, that works too!"

    c101 = CommentNode(101, "Alice",   "This recipe looks amazing!", likes=50)
    c201 = CommentNode(201, "Bob",     "I tried it last night!", likes=30)
    c301 = CommentNode(301, "Alice",   "What did you think?", likes=10)
    c401 = CommentNode(401, "Bob",     "It was delicious!", likes=25)
    c202 = CommentNode(202, "Charlie", "Can I use olive oil instead?", likes=15)
    c302 = CommentNode(302, "Alice",   "Yes, that works too!", likes=8)

    c301.add_reply(c401)
    c201.add_reply(c301)
    c202.add_reply(c302)
    c101.add_reply(c201)
    c101.add_reply(c202)

    # second thread for post 2
    c501 = CommentNode(501, "Diana", "Great post!", likes=5)
    c601 = CommentNode(601, "Bob",   "Totally agree.", likes=3)
    c501.add_reply(c601)

    # ---------- build posts -----------------------------------
    post1 = Post(1, "UserA", "Pasta recipe",     likes=120, comments_count=60, shares=40)
    post2 = Post(2, "UserB", "Travel vlog",      likes=80,  comments_count=30, shares=20)
    post3 = Post(3, "UserC", "AI tutorial",      likes=200, comments_count=90, shares=70)
    post4 = Post(4, "UserA", "Music playlist",   likes=50,  comments_count=20, shares=10)

    post1.comment_thread = [c101]
    post2.comment_thread = [c501]
    # post3 & post4 have no comments for brevity

    # ---------- analytics engine ------------------------------
    engine = EngagementAnalytics(top_n=4)
    for p in [post1, post2, post3, post4]:
        engine.add_post(p)

    # ── Priority queue: top posts ──────────────────────────────
    print("=" * 60)
    print("  TOP 3 POSTS BY ENGAGEMENT (priority queue)")
    print("=" * 60)
    for post in engine.top_posts(3):
        print(f"  {post}  score={post.engagement_score}")

    # ── Doubly-linked list: browse feed ───────────────────────
    print()
    engine.show_feed()
    print("\n  → browse forward:", engine.browse_next_top_post())
    print("  → browse forward:", engine.browse_next_top_post())
    print("  → browse backward:", engine.browse_prev_top_post())

    # ── Recursive comment analytics ───────────────────────────
    print("\n" + "=" * 60)
    print("  RECURSIVE THREAD STATS")
    print("=" * 60)
    print("\nThread display for Post 1:")
    display_thread(c101)
    stats = engine.thread_stats(post1)
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # ── Set operations ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  SET OPERATIONS – cross-post audience")
    print("=" * 60)
    cross = engine.cross_post_audience()
    if cross:
        for (pid_a, pid_b), users in cross.items():
            print(f"  Posts {pid_a} & {pid_b} share commenters: {users}")
    else:
        print("  No users commented on more than one post.")

    print("\n  Top active users (post count):")
    for count, uid in engine.top_active_users(3):
        print(f"    user={uid}  posts={count}")

    # ── Divide & conquer globals ───────────────────────────────
    print("\n" + "=" * 60)
    print("  DIVIDE & CONQUER ANALYTICS")
    print("=" * 60)
    print(f"  Global max engagement post : {engine.global_max_engagement()}")
    print(f"  Global average engagement  : {engine.global_avg_engagement():.2f}")