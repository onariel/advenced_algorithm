# Exercise 1
from typing import List, Optional


class CommentNode:
    def __init__(self, comment_id, user_id, content, timestamp, likes):
        self.comment_id = comment_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.replies: List["CommentNode"] = []

    def add_reply(self, reply):
        self.replies.append(reply)


def display_thread(comment: CommentNode, level: int = 0):
    print("  " * level + f"{comment.content} (likes: {comment.likes})")
    for reply in comment.replies:
        display_thread(reply, level + 1)


def count_and_likes(comment: CommentNode):
    count = 1
    total_likes = comment.likes

    for reply in comment.replies:
        c, l = count_and_likes(reply)
        count += c
        total_likes += l

    return count, total_likes


def find_deepest_reply(comment: CommentNode) -> int:
    if not comment.replies:
        return 1

    max_depth = 0
    for reply in comment.replies:
        depth = find_deepest_reply(reply)
        if depth > max_depth:
            max_depth = depth

    return max_depth + 1


def search_by_user(comment: CommentNode, user_id, result=None):
    if result is None:
        result = []

    if comment.user_id == user_id:
        result.append(comment)

    for reply in comment.replies:
        search_by_user(reply, user_id, result)

    return result


def contains_keyword(comment: CommentNode, keyword: str) -> bool:
    if keyword.lower() in comment.content.lower():
        return True

    for reply in comment.replies:
        if contains_keyword(reply, keyword):
            return True

    return False


def delete_comment(comment: CommentNode, comment_id) -> Optional[CommentNode]:
    if comment.comment_id == comment_id:
        return None

    new_replies = []
    for reply in comment.replies:
        updated = delete_comment(reply, comment_id)
        if updated is not None:
            new_replies.append(updated)

    comment.replies = new_replies
    return comment



if __name__ == "__main__":
  
    root = CommentNode(101, "Alice", "This recipe looks amazing!", "t1", 10)

    r1 = CommentNode(201, "Bob", "I tried it last night!", "t2", 5)
    r2 = CommentNode(202, "Charlie", "Can I use olive oil?", "t3", 3)

    r11 = CommentNode(301, "Alice", "What did you think?", "t4", 4)
    r111 = CommentNode(401, "Bob", "It was delicious!", "t5", 6)

    r21 = CommentNode(302, "Alice", "Yes, that works!", "t6", 2)

    root.add_reply(r1)
    root.add_reply(r2)

    r1.add_reply(r11)
    r11.add_reply(r111)

    r2.add_reply(r21)

    print("Thread:")
    display_thread(root)

    count, likes = count_and_likes(root)
    print("\nTotal comments:", count)
    print("Total likes:", likes)

   
    print("\nMax depth:", find_deepest_reply(root))

    results = search_by_user(root, "Alice")
    print("\nComments by Alice:", len(results))

   
    print("\nContains 'delicious':", contains_keyword(root, "delicious"))

    root = delete_comment(root, 201)
    print("\nAfter deletion:")
    display_thread(root)
