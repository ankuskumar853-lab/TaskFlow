from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db
from ai_parser import parse_task


router = APIRouter(
    prefix="/tasks",
    tags=["AI Quick Add"]
)


@router.post("/quick-add")
def quick_add_preview(
    request: schemas.QuickAddRequest,
    db: Session = Depends(get_db)
):

    # ==========================
    # Check Project
    # ==========================

    project = db.query(models.Project).filter(
        models.Project.id == request.project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=422,
            detail="Project not found"
        )

    # ==========================
    # Mock AI Parser
    # ==========================

    parsed = parse_task(request.description)

    # ==========================
    # Return Preview Only
    # ==========================

    return {
        "title": parsed["title"],
        "description": request.description,
        "priority": parsed.get("priority", "medium"),
        "due_date": parsed.get("due_date"),
        "project_id": request.project_id
    }