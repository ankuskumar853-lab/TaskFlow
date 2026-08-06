from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator


# ==========================
# User Schemas
# ==========================
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True


# ==========================
# Project Schemas
# ==========================
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    owner_id: int


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True


# ==========================
# Task Schemas
# ==========================
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    status: str = "pending"
    priority: Literal["low", "medium", "high"]
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[str] = None


class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True

class QuickAddRequest(BaseModel):
    text: str
    project_id: int


class QuickAddResponse(BaseModel):
    message: str
    task_id: int
    title: str
    priority: str
    due_date: str | None = None        


# ==========================
# AI Quick Add
# ==========================
class QuickAddRequest(BaseModel):
    description: str = Field(..., min_length=1)
    project_id: int


# ==========================
# Statistics Response
# ==========================
class ProjectStats(BaseModel):
    id: int
    name: str
    task_count: int

