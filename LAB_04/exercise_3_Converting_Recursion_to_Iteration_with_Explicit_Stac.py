import datetime
import random
class CommentNone:

    def __init__(self, user_id, content, timestamp, likes):
        self.comment_id = random.randint(1, 1000)
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.replies = []

    def addReplies(self, comment):
        self.replies.append(comment)

    def getReplies(self):
        return self.replies

class thread:

    def __init__(self):
        self.comments = []

    def addComment(self, comment):
        self.comments.append(comment)


def getComments_rec(comment, comments = None):
    if comments is None:
        comments = []
    comments += [comment.content]
    for replie in comment.getReplies():
        getComments_rec(replie, comments)
    return comments

def getComments_it(comment):
    comments = []
    stack = [comment]
    while stack != []:
        curr_comment = stack.pop()
        comments.append(curr_comment.content)
        for replie in reversed(curr_comment.getReplies()):
            stack.append(replie)
    return comments

def big_node(depth, child, c_main):
    if depth == 0:
        return 0
    for i in range(child):
        c_next = CommentNone(i, "c" + str(depth) + "_" + str(i), datetime.datetime.now(), i)
        c_main.addReplies(c_next)
        big_node(depth - 1, child, c_next)
    return 0

def test_depth(depth, child, c_main):
    c_main = CommentNone(1, "c_main", datetime.datetime.now(), 5)
    big_node(depth, child, c_main)

    start = datetime.datetime.now()
    getComments_it(c_main)
    end = datetime.datetime.now()
    print(f"depth={depth}, child={child} | iterative:  {end - start}")

    start = datetime.datetime.now()
    getComments_rec(c_main)
    end = datetime.datetime.now()
    print(f"depth={depth}, child={child} | recursive: {end - start}")

c1 = CommentNone(1, "c1", datetime.datetime.now(), 1)
c2 = CommentNone(2, "c2", datetime.datetime.now(), 2)
c3 = CommentNone(3, "c3", datetime.datetime.now(), 3)
c4 = CommentNone(4, "c4", datetime.datetime.now(), 4)
c5 = CommentNone(5, "c1_1", datetime.datetime.now(), 5)
c6 = CommentNone(6, "c2_1", datetime.datetime.now(), 6)
c7 = CommentNone(7, "c3_1", datetime.datetime.now(), 7)
c8 = CommentNone(8, "c1_1_1", datetime.datetime.now(), 8)
c9 = CommentNone(9, "c1_2", datetime.datetime.now(), 9)
c10 = CommentNone(10, "c1_2_1", datetime.datetime.now(), 10)
c11 = CommentNone(12, "c1_2_1_1", datetime.datetime.now(), 11)
c_main = CommentNone(1, "c_main", datetime.datetime.now(), 5)

c1.addReplies(c5)
c2.addReplies(c6)
c3.addReplies(c7)
c5.addReplies(c8)
c1.addReplies(c9)
c9.addReplies(c10)
c10.addReplies(c11)

print(getComments_rec(c1))
print(getComments_it(c1))

test_depth(5, 1, c_main)
test_depth(10, 1, c_main)
test_depth(50, 1, c_main)
test_depth(100, 1, c_main)
test_depth(500, 1, c_main)

test_depth(20, 2, c_main)