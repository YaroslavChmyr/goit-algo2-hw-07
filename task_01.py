import random
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def invalidate(self, index):
        keys_to_remove = [key for key in self.cache if index in range(key[0], key[1] + 1)]
        for key in keys_to_remove:
            del self.cache[key]

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R, cache):
    cached_result = cache.get((L, R))
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put((L, R), result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate(index)

N = 100000
Q = 50000
array = [random.randint(1, 1000) for _ in range(N)]
queries = [("Range", random.randint(0, N-1), random.randint(0, N-1)) if random.random() < 0.7 else ("Update", random.randint(0, N-1), random.randint(1, 1000)) for _ in range(Q)]

queries = [(t, min(L, R), max(L, R)) if t == "Range" else (t, L, R) for t, L, R in queries]

start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
execution_time_no_cache = time.time() - start_time

cache = LRUCache(1000)
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(array, query[1], query[2], cache)
    else:
        update_with_cache(array, query[1], query[2], cache)
execution_time_with_cache = time.time() - start_time

print(f"Час виконання без кешування: {execution_time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {execution_time_with_cache:.2f} секунд")

