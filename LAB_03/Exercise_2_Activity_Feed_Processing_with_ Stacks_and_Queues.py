class StackNode:
    def __init__(self, activity):
        self.activity = activity
        self.next = None
      
class ActivityStack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, activity):
        new_node = StackNode(activity)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        if self.top is None:
            return None

        temp = self.top
        self.top = self.top.next
        self.size -= 1
        return temp.activity

    def peek(self):
        if self.top:
            return self.top.activity
        return None

    def is_empty(self):
        return self.top is None

    def display_recent(self, n):
        temp = self.top
        count = 0

        while temp and count < n:
            print(temp.activity)
            temp = temp.next
            count += 1

class QueueNode:
    def __init__(self, notification):
        self.notification = notification
        self.next = None

class NotificationQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, notification):
        new_node = QueueNode(notification)

        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None

        temp = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        self.size -= 1
        return temp.notification

    def priority_enqueue(self, notification):
        new_node = QueueNode(notification)
        new_node.next = self.front
        self.front = new_node

        if self.rear is None:
            self.rear = new_node

        self.size += 1

    def display_pending(self):
        temp = self.front
        while temp:
            print(temp.notification)
            temp = temp.next


class FeedProcessor:
    def __init__(self):
        self.recent_activities = ActivityStack()
        self.notification_queue = NotificationQueue()
        self.processed_log = NotificationQueue()

    def process_incoming(self):
        notif = self.notification_queue.dequeue()
        if notif:
            self.recent_activities.push(notif)

    def batch_process(self, k):
        count = 0
        while count < k and not self.notification_queue.front is None:
            notif = self.notification_queue.dequeue()
            self.recent_activities.push(notif)
            count += 1

    def clear_history(self):
        while not self.recent_activities.is_empty():
            action = self.recent_activities.pop()
            self.processed_log.enqueue(action)

    def get_stats(self):
        print("Recent Activities:", self.recent_activities.size)
        print("Pending Notifications:", self.notification_queue.size)
        print("Processed Items:", self.processed_log.size)

feed = FeedProcessor()

feed.notification_queue.enqueue("New follower")
feed.notification_queue.enqueue("New like")
feed.notification_queue.enqueue("New comment")

feed.process_incoming()

feed.batch_process(2)

feed.recent_activities.display_recent(5)

feed.clear_history()

feed.get_stats()
