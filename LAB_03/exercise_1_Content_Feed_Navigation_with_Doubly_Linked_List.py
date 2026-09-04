import datetime
import random


class stoy_node:
    def __init__(self, user_id, content_preview, timestamp):
        self.story_id = random.randint(1, 800000000)
        self.user_id = user_id
        self.content_preview = content_preview
        self.timestamp = timestamp
        self.views = 0
        self.next = None
        self.prev = None

    def get_id(self):
        return self.story_id

    def add_view(self):
        self.views += 1

    def __str__(self):
        return "id: " + str(self.story_id) + " user_id: " + str(
            self.user_id) + " content_preview: " + self.content_preview + " views: " + str(self.views)


class feed:
    def __init__(self, node):
        self.head = node
        self.tail = node
        self.size = 1
        self.current = node
        node.add_view()

    def add_story(self, story):
        self.size += 1
        self.tail.next = story
        story.prev = self.tail
        self.tail = story
        return "story added successfully"

    def remove_story(self, story):
        if self.size == 1:
            return "you cannot make an empty feed"
        pointer = self.head
        if pointer == story:
            if self.current == story:
                self.current = pointer.next
            self.head = pointer.next
            pointer.next.prev = None
            self.size -= 1
            return "story removed successfully"
        pointer = pointer.next
        for i in range(self.size):
            if pointer == story:
                if pointer.next:
                    if self.current == story:
                        self.current = pointer.next
                    pointer.prev.next = pointer.next
                    pointer.next.prev = pointer.prev
                else:
                    if self.current == story:
                        self.current = pointer.prev
                    pointer.prev.next = None

                self.size -= 1
                return "story removed successfully"
            else:
                pointer = pointer.next
        return "story not found"

    def move_foward(self):
        if self.current == self.tail:
            return "you are on the the last story of the feed, you cannot go further"
        self.current = self.current.next
        self.current.add_view()
        return self.current.__str__()

    def move_backward(self):
        if self.current == self.head:
            return "you are on the the first story of the feed, you cannot go further"
        self.current = self.current.prev
        self.current.add_view()
        return self.current.__str__()

    def jump_to(self, story_id):
        pointer = self.head
        for i in range(self.size):
            if pointer.get_id() == story_id:
                self.current = pointer
                self.current.add_view()
                return pointer
            pointer = pointer.next
        return "story not found"

    def insert_after(self, story_id, new_story):
        pointer = self.head
        for i in range(self.size + 2):
            if pointer.get_id() == story_id:
                if pointer == self.tail:
                    self.tail = new_story
                    pointer.next = new_story
                    self.tail.prev = pointer
                    self.size += 1
                    return "story added successfully"
                new_story.next = pointer.next
                pointer.next.prev = new_story
                pointer.next = new_story
                pointer.next.prev = pointer
                self.size += 1
                return "story added successfully"
            pointer = pointer.next
        return "story not found"

    def display_around_current(self):
        return "prev :" + self.current.prev.__str__() + " next : " + self.current.next.__str__()

    def track_view(self):
        return "the current post has " + str(self.current.views) + " views"

    def most_reviewed(self):
        most_reviewed = self.current.prev
        pointer = self.head
        for i in range(self.size):
            if pointer.views > most_reviewed.views:
                most_reviewed = pointer
        return most_reviewed.__str__()

    def reorder_by_views(self):
        for i in range(self.size - 1):
            pointer = self.head
            for n in range(i):
                pointer = pointer.next
            less_reviewed = pointer
            for j in range(i, self.size - 1):
                if pointer.views < less_reviewed.views:
                    less_reviewed = pointer
                pointer = pointer.next

            if less_reviewed == self.tail:
                self.tail = less_reviewed.prev
            if less_reviewed.prev:
                if less_reviewed.next:
                    less_reviewed.prev.next = less_reviewed.next
                    less_reviewed.next.prev = less_reviewed.prev
                else:
                    less_reviewed.prev.next = None
            less_reviewed.next = self.head
            less_reviewed.prev = None
            self.head.prev = less_reviewed
            self.head = less_reviewed

    def link_check(self):
        head_ids = []
        tails_ids = []
        head_pointer = self.head
        tail_pointer = self.tail
        for i in range(self.size - 1):
            head_ids.append(head_pointer.content_preview)
            tails_ids.append(tail_pointer.content_preview)
            head_pointer = head_pointer.next
            tail_pointer = tail_pointer.prev
        tails_ids.reverse()
        if head_ids == tails_ids:
            return "the feed is well ordered"
        return "you messed up"

    def __str__(self):
        string = ""
        pointer = self.head
        while pointer:
            string += pointer.__str__() + " prev: " + pointer.prev.__str__() + " next: " + pointer.next.__str__() + " \n"
            pointer = pointer.next
        return string


story1 = stoy_node(1, "story1", datetime.datetime.now())
story2 = stoy_node(2, "story2", datetime.datetime.now())
story3 = stoy_node(3, "story3", datetime.datetime.now())
story4 = stoy_node(4, "story4", datetime.datetime.now())
story5 = stoy_node(5, "story5", datetime.datetime.now())
story6 = stoy_node(6, "story6", datetime.datetime.now())
main_feed = feed(story1)
print(main_feed.add_story(story2))
print(main_feed.add_story(story3))
print(main_feed.add_story(story5))
print(main_feed.add_story(story6))
print(main_feed)
print(main_feed.current)
print(main_feed.move_foward())
print(main_feed.move_backward())
print(main_feed.move_backward())
main_feed.jump_to(story3.get_id())
main_feed.jump_to(story3.get_id())
main_feed.jump_to(story3.get_id())
print(main_feed.current)
print(main_feed.insert_after(story3.get_id(), story4))
print(main_feed.link_check())
print(main_feed.display_around_current())
print(main_feed.track_view())
print(main_feed.most_reviewed())
print(main_feed.link_check())
print("--------------------")
print(main_feed)
main_feed.reorder_by_views()
print("feed after reordering: \n \n", main_feed)
