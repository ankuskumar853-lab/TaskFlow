import random
import time

from algorithms import insertion_sort, binary_search, linear_search


# 1000 random records
records = []

for i in range(1000):
    records.append({
        "title": f"Task {i}",
        "priority": random.randint(1, 3)
    })


# --------------------------
# Insertion Sort
# --------------------------
sort_data = records.copy()

start = time.perf_counter()

insertion_sort(sort_data, "priority")

end = time.perf_counter()

print(f"Insertion Sort: {end-start:.6f} sec")


# --------------------------
# Binary Search
# --------------------------
sort_data = sorted(records, key=lambda x: x["title"])

start = time.perf_counter()

binary_search(sort_data, "Task 500", "title")

end = time.perf_counter()

print(f"Binary Search: {end-start:.6f} sec")


# --------------------------
# Linear Search
# --------------------------
start = time.perf_counter()

linear_search(records, "Task 500", "title")

end = time.perf_counter()

print(f"Linear Search: {end-start:.6f} sec")