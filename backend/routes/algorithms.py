from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from algorithms import insertion_sort, binary_search, linear_search

router = APIRouter(
    prefix="/algorithms",
    tags=["Algorithms"]
)


# Sort Tasks By Priority
@router.get("/tasks/sort")
def sort_tasks(db: Session = Depends(get_db)):

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

    insertion_sort(records, "priority")

    return records


# Search Task
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

    else:

        index = linear_search(
            records,
            title,
            "title"
        )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return records[index]