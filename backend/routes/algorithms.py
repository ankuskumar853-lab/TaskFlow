from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from algorithms import insertion_sort, binary_search, linear_search


router = APIRouter(
    tags=["Algorithms"]
)


# =========================
# Sort Tasks By Priority
# GET /tasks?sort=priority
# =========================

@router.get("/tasks")
def get_tasks_sorted(
    sort: str | None = None,
    db: Session = Depends(get_db)
):

    tasks = db.query(models.Task).all()

    records = []

    priority_rank = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    for task in tasks:
        records.append({
            "id": task.id,
            "title": task.title,
            "priority": priority_rank[task.priority],
            "priority_name": task.priority,
            "due_date": task.due_date
        })

    if sort == "priority":
        insertion_sort(records, "priority")

    return records


# =========================
# Search Task
# GET /tasks/search?title=...&algo=binary
# =========================

@router.get("/tasks/search")
def search_task(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):

    tasks = db.query(models.Task).all()

    records = []

    for task in tasks:
        records.append({
            "id": task.id,
            "title": task.title
        })

    if algo == "binary":

        insertion_sort(records, "title")

        index = binary_search(
            records,
            title,
            "title"
        )

    elif algo == "linear":

        index = linear_search(
            records,
            title,
            "title"
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="algo must be binary or linear"
        )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return records[index]