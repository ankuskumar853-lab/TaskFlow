from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# Create Project
@router.post("/", response_model=schemas.ProjectResponse, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):

    # Check Owner Exists
    owner = db.query(models.User).filter(models.User.id == project.owner_id).first()

    if owner is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# Get All Projects
@router.get("/", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()