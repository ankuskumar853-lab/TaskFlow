from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from database import get_db
from auth import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =========================================================
# HELPER: CHECK PROJECT OWNERSHIP
# =========================================================

def get_owned_project(
    project_id: int,
    current_user: models.User,
    db: Session
):

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.owner_id == current_user.id
        )
        .first()
    )

    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


# =========================================================
# CREATE TASK
# =========================================================

@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=201
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    print("CREATE TASK:", task)

    # Check project belongs to current user
    get_owned_project(
        task.project_id,
        current_user,
        db
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

    print("TASK CREATED:", new_task.id)

    return new_task


# =========================================================
# AI QUICK ADD
# =========================================================

@router.post("/quick-add")
def quick_add_task(
    request: schemas.QuickAddRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    print("QUICK ADD REQUEST:", request)

    description = request.description.strip()

    if not description:
        raise HTTPException(
            status_code=400,
            detail="Description cannot be empty"
        )

    # Check project belongs to current user
    get_owned_project(
        request.project_id,
        current_user,
        db
    )

    text = description.lower()

    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    if (
        "high priority" in text
        or "urgent" in text
        or "high" in text
    ):
        priority = "high"

    elif (
        "low priority" in text
        or "low" in text
    ):
        priority = "low"

    else:
        priority = "medium"

    # -----------------------------------------------------
    # DUE DATE
    # -----------------------------------------------------

    due_date = None

    if "today" in text:

        due_date = (
            datetime.now().date()
        ).isoformat()

    elif "tomorrow" in text:

        due_date = (
            datetime.now().date()
            + timedelta(days=1)
        ).isoformat()

    # -----------------------------------------------------
    # CREATE TITLE
    # -----------------------------------------------------

    title = description

    remove_words = [
        "high priority",
        "low priority",
        "urgent",
        "tomorrow",
        "today"
    ]

    for word in remove_words:
        title = title.replace(word, "")

    title = " ".join(title.split())

    if not title:
        title = description

    # -----------------------------------------------------
    # RETURN PREVIEW
    # -----------------------------------------------------

    result = {
        "title": title,
        "description": description,
        "status": "pending",
        "priority": priority,
        "due_date": due_date,
        "project_id": request.project_id
    }

    print("QUICK ADD RESULT:", result)

    return result


# =========================================================
# GET ALL TASKS (ONLY CURRENT USER'S TASKS)
# =========================================================

@router.get("/")
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    tasks = (
        db.query(models.Task)
        .join(
            models.Project,
            models.Task.project_id == models.Project.id
        )
        .filter(
            models.Project.owner_id == current_user.id
        )
        .order_by(models.Task.id.desc())
        .all()
    )

    priority_rank = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    records = []

    for task in tasks:

        records.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "project_id": task.project_id
        })

    # -----------------------------------------------------
    # SORT BY PRIORITY
    # -----------------------------------------------------

    if sort == "priority":

        records.sort(
            key=lambda x: priority_rank.get(
                x["priority"],
                0
            ),
            reverse=True
        )

    # -----------------------------------------------------
    # SORT BY OLDEST
    # -----------------------------------------------------

    elif sort == "oldest":

        records.sort(
            key=lambda x: x["id"]
        )

    # -----------------------------------------------------
    # SORT BY NEWEST
    # -----------------------------------------------------

    elif sort == "newest":

        records.sort(
            key=lambda x: x["id"],
            reverse=True
        )

    # -----------------------------------------------------
    # PENDING FIRST
    # -----------------------------------------------------

    elif sort == "status":

        records.sort(
            key=lambda x: (
                0
                if x["status"] == "pending"
                else 1
            )
        )

    return records


# =========================================================
# SEARCH TASK (ONLY CURRENT USER'S TASKS)
# =========================================================

@router.get("/search")
def search_task(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    from algorithms import (
        insertion_sort,
        binary_search,
        linear_search
    )

    tasks = (
        db.query(models.Task)
        .join(
            models.Project,
            models.Task.project_id == models.Project.id
        )
        .filter(
            models.Project.owner_id == current_user.id
        )
        .all()
    )

    records = []

    for task in tasks:

        records.append({
            "id": task.id,
            "title": task.title
        })

    if not records:

        raise HTTPException(
            status_code=404,
            detail="No tasks available"
        )

    # -----------------------------------------------------
    # BINARY SEARCH
    # -----------------------------------------------------

    if algo == "binary":

        insertion_sort(
            records,
            "title"
        )

        index = binary_search(
            records,
            title,
            "title"
        )

    # -----------------------------------------------------
    # LINEAR SEARCH
    # -----------------------------------------------------

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

    task_id = records[index]["id"]

    task = (
        db.query(models.Task)
        .join(
            models.Project,
            models.Task.project_id == models.Project.id
        )
        .filter(
            models.Task.id == task_id,
            models.Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "project_id": task.project_id
    }


# =========================================================
# PROJECT STATISTICS (ONLY CURRENT USER'S PROJECTS)
# =========================================================

@router.get("/stats/projects")
def get_project_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    stats = (
        db.query(
            models.Project.id,
            models.Project.name,
            func.count(models.Task.id).label(
                "task_count"
            )
        )
        .outerjoin(
            models.Task,
            models.Task.project_id
            == models.Project.id
        )
        .filter(
            models.Project.owner_id == current_user.id
        )
        .group_by(
            models.Project.id,
            models.Project.name
        )
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


# =========================================================
# GET SINGLE TASK (ONLY IF OWNED BY CURRENT USER)
# =========================================================

@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    task = (
        db.query(models.Task)
        .join(
            models.Project,
            models.Task.project_id == models.Project.id
        )
        .filter(
            models.Task.id == task_id,
            models.Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =========================================================
# UPDATE TASK (ONLY IF OWNED BY CURRENT USER)
# =========================================================

@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    print(
        "UPDATE TASK:",
        task_id,
        updated_task
    )

    task = (
        db.query(models.Task)
        .join(
            models.Project,
            models.Task.project_id == models.Project.id
        )
        .filter(
            models.Task.id == task_id,
            models.Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = (
        updated_task
        .model_dump(
            exclude_unset=True
        )
    )

    # -----------------------------------------------------
    # If project_id is being changed
    # -----------------------------------------------------

    if "project_id" in update_data:

        get_owned_project(
            update_data["project_id"],
            current_user,
            db
        )

    # -----------------------------------------------------
    # Update fields
    # -----------------------------------------------------

    for key, value in update_data.items():

        setattr(
            task,
            key,
            value
        )

    db.commit()
    db.refresh(task)

    print(
        "TASK UPDATED:",
        task.id
    )

    return task


# =========================================================
# DELETE TASK (ONLY IF OWNED BY CURRENT USER)
# =========================================================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    print(
        "DELETE TASK:",
        task_id
    )

    task = (
        db.query(models.Task)
        .join(
            models.Project,
            models.Task.project_id == models.Project.id
        )
        .filter(
            models.Task.id == task_id,
            models.Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    print(
        "TASK DELETED:",
        task_id
    )

    return {
        "message": "Task deleted successfully",
        "id": task_id
    }