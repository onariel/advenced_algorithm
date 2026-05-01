import math
import random
import time
from typing import List, Optional, Tuple

class HeapEntry:
    def __init__(self, likes: int, post_id: str, timestamp: int):
        self.likes = likes
        self.post_id = post_id
        self.timestamp = timestamp

class TrendingHeap:
    def __init__(self):
        self.heap: List[HeapEntry] = []
        self.size: int = 0

def parent(i: int) -> int:
    return (i - 1) // 2

def left_child(i: int) -> int:
    return 2 * i + 1

def right_child(i: int) -> int:
    return 2 * i + 2

def swap(heap: List[HeapEntry], i: int, j: int) -> None:
    """Swap two elements in the heap list"""
    temp = heap[i]
    heap[i] = heap[j]
    heap[j] = temp

def heap_up(heap: List[HeapEntry], index: int) -> None:
    """When inserting a new element at the end, ensure heap property by likes"""
    while index > 0:
        p = parent(index)
        if heap[index].likes > heap[p].likes:
            swap(heap, index, p)
            index = p
        else:
            break

def heap_down(heap: List[HeapEntry], index: int, heap_size: int) -> None:
    """When deleting the root, re-heapify by likes"""
    largest = index
    left = left_child(index)
    right = right_child(index)
    
    # Compare with left child
    if left < heap_size and heap[left].likes > heap[largest].likes:
        largest = left
    
    # Compare with right child
    if right < heap_size and heap[right].likes > heap[largest].likes:
        largest = right
    
    # If largest is not the current index, swap and continue
    if largest != index:
        swap(heap, index, largest)
        heap_down(heap, largest, heap_size)

def find_index(heap: List[HeapEntry], post_id: str) -> int:
    """Find the index of a post by its post_id"""
    for i in range(len(heap)):
        if heap[i].post_id == post_id:
            return i
    return -1

def initialize(heap: TrendingHeap) -> None:
    """Initialize an empty TrendingHeap"""
    heap.heap = []
    heap.size = 0

def push(heap: TrendingHeap, post_id: str, likes: int, timestamp: int) -> None:
    """Insert a new post into the heap"""
    new_entry = HeapEntry(likes, post_id, timestamp)
    heap.heap.append(new_entry)
    heap.size += 1
    heap_up(heap.heap, heap.size - 1)

def pop_max(heap: TrendingHeap) -> Optional[HeapEntry]:
    """Remove and return the post with maximum likes"""
    if heap.size == 0:
        return None
    
    max_entry = heap.heap[0]
    heap.heap[0] = heap.heap[heap.size - 1]
    heap.heap.pop()  # Remove last element
    heap.size -= 1
    
    if heap.size > 0:
        heap_down(heap.heap, 0, heap.size)
    
    return max_entry

def peek_max(heap: TrendingHeap) -> Optional[HeapEntry]:
    """Return the post with maximum likes without removing it"""
    if heap.size == 0:
        return None
    return heap.heap[0]

def get_top_k(heap: TrendingHeap, k: int) -> List[HeapEntry]:
    """Return the top k posts with maximum likes"""
    # Create a copy of the heap list
    temp_heap = heap.heap.copy()
    result = []
    effective_k = min(k, heap.size)
    
    for i in range(effective_k):
        if len(temp_heap) == 0:
            break
        
        max_entry = temp_heap[0]
        temp_heap[0] = temp_heap[-1]
        temp_heap.pop()
        
        if len(temp_heap) > 0:
            heap_down(temp_heap, 0, len(temp_heap))
        
        result.append(max_entry)
    
    return result

def update_likes(heap: TrendingHeap, post_id: str, new_likes: int, new_timestamp: int) -> None:
    """Update the likes of a specific post"""
    index = find_index(heap.heap, post_id)
    if index == -1:
        return
    
    old_likes = heap.heap[index].likes
    
    # Update the post
    heap.heap[index].likes = new_likes
    heap.heap[index].timestamp = new_timestamp
    
    # Re-heapify based on whether likes increased or decreased
    if new_likes > old_likes:
        heap_up(heap.heap, index)
    else:
        heap_down(heap.heap, index, heap.size)

def size(heap: TrendingHeap) -> int:
    return heap.size

def is_valid_heap(heap: TrendingHeap) -> bool:
    """Check if the heap satisfies the max-heap property"""
    n = heap.size
    for i in range(n // 2):
        left = left_child(i)
        right = right_child(i)
        
        if left < n and heap.heap[i].likes < heap.heap[left].likes:
            return False
        
        if right < n and heap.heap[i].likes < heap.heap[right].likes:
            return False
    
    return True

def get_height(heap: TrendingHeap) -> int:
    """Return the height of the heap tree"""
    if heap.size == 0:
        return 0
    return math.floor(math.log2(heap.size)) + 1

def get_level_order(heap: TrendingHeap) -> List[List[HeapEntry]]:
    """Return the heap elements in level order traversal"""
    result = []
    level = 0
    start = 0
    elements_per_level = 1
    
    while start < heap.size:
        end = min(start + elements_per_level, heap.size)
        level_elements = heap.heap[start:end]
        result.append(level_elements)
        start = end
        elements_per_level *= 2
        level += 1
    
    return result


# test cases

if __name__ == "__main__":
   # random.seed(42)
    
    
    # 1. Create initial post
    print("\n1. Start with 100 posts...")
    heap = TrendingHeap()
    initialize(heap)
    
    for i in range(100):
        post_id = f"post_{i:03d}"
        likes = random.randint(0, 1000)
        timestamp = i
        push(heap, post_id, likes, timestamp)
    
    print(f"    {size(heap)} posts have been created.")
    
    # Display initial top 5
    print("\n--- Initial top 5 ---")
    top_5 = get_top_k(heap, 5)
    for idx, post in enumerate(top_5, 1):
        print(f"  {idx}. {post.post_id}: {post.likes} likes")
    
    # 2. Perform 10,000 like updates
    print("\n2. Perform 10,000 like updates ...")
    
    # Get a list of all post IDs
    post_ids = [f"post_{i:03d}" for i in range(100)]
    
    # Recording time
    update_times = []
    query_times = []
    
    total_updates = 10000
    query_interval = 1000
    
    for i in range(1, total_updates + 1):
        post_id = random.choice(post_ids)
        
        increment = random.randint(1, 50)
        
        index = find_index(heap.heap, post_id)
        if index != -1:
            current_likes = heap.heap[index].likes
            new_likes = current_likes + increment
            new_timestamp = i
            
            update_start = time.time()
            update_likes(heap, post_id, new_likes, new_timestamp)
            update_time = time.time() - update_start
            update_times.append(update_time)
        
        # Query and display the top 5 after every 1000 updates.
        if i % query_interval == 0:
            query_start = time.time()
            
            print(f"\n--- the {i // query_interval}times query (already  updated {i} times) ---")
            top_5 = get_top_k(heap, 5)
            print("Top 5 Popular posts:")
            for idx, post in enumerate(top_5, 1):
                print(f"  {idx}. {post.post_id}: {post.likes} likes")
            
            query_time = time.time() - query_start
            query_times.append(query_time)
            
            # Display progress
            progress = (i / total_updates) * 100
            print(f"  progress rate: {progress:.1f}% ({i}/{total_updates})")
    

    # 3. Display statistics
    avg_update_time = sum(update_times) / len(update_times) if update_times else 0
    avg_query_time = sum(query_times) / len(query_times) if query_times else 0
    
    print(f"  - Total number of updates: {total_updates}")
    print(f"  - Total number of queries: {len(query_times)}")
    print(f"\nAverage time:")
    print(f"  - {avg_update_time*1000:.4f} ")
    print(f"  -  {avg_query_time*1000:.4f} ")
    
    total_time = sum(update_times) + sum(query_times)
    print(f"  - Total Time: {total_time:.4f} s")
    print(f"  - update: {total_updates/total_time:.2f} times/s")
    print(f"  - inquiry: {len(query_times)/total_time:.2f} times/s")
    

    print(f"  - Final number of posts: {size(heap)}")
    print(f"  - Height of the pile: {get_height(heap)}")
    