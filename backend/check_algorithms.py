from algorithms import (
    insertion_sort,
    binary_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")


# ==========================================
# 1. Empty list insertion sort
# ==========================================

records = []

insertion_sort(records, "priority")

check(
    "insertion_sort empty list",
    records,
    []
)


# ==========================================
# 2. Single element insertion sort
# ==========================================

records = [
    {"title": "Task 1", "priority": 2}
]

insertion_sort(records, "priority")

check(
    "insertion_sort single element",
    records,
    [{"title": "Task 1", "priority": 2}]
)


# ==========================================
# Sorted records for binary search
# ==========================================

records = [
    {"title": "A"},
    {"title": "B"},
    {"title": "C"},
    {"title": "D"},
    {"title": "E"}
]


# ==========================================
# 3. Binary search - first index
# ==========================================

result = binary_search(
    records,
    "A",
    "title"
)

check(
    "binary_search first index",
    result,
    0
)


# ==========================================
# 4. Binary search - last index
# ==========================================

result = binary_search(
    records,
    "E",
    "title"
)

check(
    "binary_search last index",
    result,
    4
)


# ==========================================
# 5. Binary search - middle index
# ==========================================

result = binary_search(
    records,
    "C",
    "title"
)

check(
    "binary_search middle index",
    result,
    2
)


# ==========================================
# 6. Binary search - not found
# ==========================================

result = binary_search(
    records,
    "Z",
    "title"
)

check(
    "binary_search not found",
    result,
    -1
)


# ==========================================
# 7. Insertion sort count
# ==========================================

records = [
    {"title": "C", "priority": 3},
    {"title": "A", "priority": 1},
    {"title": "B", "priority": 2}
]

result = insertion_sort_count(
    records,
    "priority"
)

expected_records = [
    {"title": "A", "priority": 1},
    {"title": "B", "priority": 2},
    {"title": "C", "priority": 3}
]

check(
    "insertion_sort_count sorted list",
    records,
    expected_records
)

if type(result) == int and result > 0:
    print("PASS: insertion_sort_count comparison count")
else:
    print(
        f"FAIL: insertion_sort_count comparison count "
        f"— expected positive int, got {result}"
    )


# ==========================================
# 8. Binary search count
# ==========================================

records = [
    {"title": "A"},
    {"title": "B"},
    {"title": "C"},
    {"title": "D"},
    {"title": "E"}
]

result = binary_search_count(
    records,
    "C",
    "title"
)

if (
    result["index"] == 2
    and type(result["comparison_count"]) == int
    and result["comparison_count"] > 0
):
    print("PASS: binary_search_count")
else:
    print(
        f"FAIL: binary_search_count "
        f"— got {result}"
    )


# ==========================================
# 9. Linear search count - not found
# ==========================================

records = [
    {"title": "A"},
    {"title": "B"},
    {"title": "C"},
    {"title": "D"},
    {"title": "E"}
]

result = linear_search_count(
    records,
    "Z",
    "title"
)

if (
    result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: linear_search_count not found")
else:
    print(
        f"FAIL: linear_search_count not found "
        f"— got {result}"
    )