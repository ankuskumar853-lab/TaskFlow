from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db
from ai_parser import parse_task

router = APIRouter(
    prefix="/quick-add",
    tags=["AI Quick Add"]
)


@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def quick_add_task(
    request: schemas.QuickAddRequest,
    db: Session = Depends(get_db)
):

    # Check Project Exists
    project = db.query(models.Project).filter(
        models.Project.id == request.project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # AI Parser
    parsed = parse_task(request.description)

    # Create Task
    task = models.Task(
        title=parsed["title"],
        description=request.description,
        status="pending",
        priority=parsed["priority"],
        due_date=parsed["due_date"],
        project_id=request.project_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task