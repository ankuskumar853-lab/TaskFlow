import random

from algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


# ==========================================
# Create TaskFlow-like Test Data
# ==========================================

def generate_records(size):
    records = []

    for i in range(size):
        records.append({
            "title": f"Task {i}",
            "priority": random.randint(1, 3),
            "due_date": "tomorrow"
        })

    return records


# ==========================================
# Run Benchmark
# ==========================================

sizes = [10, 500, 3000]

for size in sizes:

    print("\n" + "=" * 50)
    print(f"DATA SIZE: {size}")
    print("=" * 50)

    records = generate_records(size)

    # --------------------------------------
    # Insertion Sort Count
    # --------------------------------------

    sort_records = records.copy()

    insertion_comparisons = insertion_sort_count(
        sort_records,
        "priority"
    )

    print(
        f"Insertion Sort comparisons: "
        f"{insertion_comparisons}"
    )

    # --------------------------------------
    # Binary Search Count
    # --------------------------------------

    binary_records = records.copy()

    # First sort using the same insertion sort
    insertion_sort_count(
        binary_records,
        "title"
    )

    target = f"Task {size // 2}"

    binary_result = binary_search_count(
        binary_records,
        target,
        "title"
    )

    print(
        f"Binary Search: "
        f"index={binary_result['index']}, "
        f"comparisons={binary_result['comparison_count']}"
    )

    # --------------------------------------
    # Linear Search Count
    # --------------------------------------

    linear_result = linear_search_count(
        records,
        target,
        "title"
    )

    print(
        f"Linear Search: "
        f"index={linear_result['index']}, "
        f"comparisons={linear_result['comparison_count']}"
    )