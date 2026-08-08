from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



# Create Task
@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    print("Project ID:", task.project_id)
    print("Task Data:", task)

    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/")
def get_tasks(
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
        from algorithms import insertion_sort
        insertion_sort(records, "priority")

    return records

@router.get("/search")
def search_task(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):
    from algorithms import (
        insertion_sort,
        binary_search,
        linear_search
    )

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

# ==========================
# Project Statistics
# ==========================
@router.get("/stats/projects")
def get_project_stats(db: Session = Depends(get_db)):

    stats = (
        db.query(
            models.Project.id,
            models.Project.name,
            func.count(models.Task.id).label("task_count")
        )
        .outerjoin(models.Task)
        .group_by(models.Project.id)
        .all()
    )

    result = []

    for project in stats:
        result.append({
            "project_id": project.id,
            "project_name": project.name,
            "task_count": project.task_count
        })

    return result


# Get Task By ID
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# ==========================
# Update Task
# ==========================
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = updated_task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# ==========================
# Delete Task
# ==========================
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }



