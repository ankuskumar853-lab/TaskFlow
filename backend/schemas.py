from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator


# ==========================================
# USER SCHEMAS
# ==========================================

class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: str

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ==========================================
# LOGIN SCHEMA
# ==========================================

class LoginRequest(BaseModel):
    email: str
    password: str


# ==========================================
# TOKEN RESPONSE
# ==========================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ==========================================
# PROJECT SCHEMAS
# ==========================================

class ProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    owner_id: int


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# TASK SCHEMAS
# ==========================================

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = None

    status: str = "pending"

    priority: Literal[
        "low",
        "medium",
        "high"
    ]

    due_date: Optional[str] = None

    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Title cannot be empty"
            )

        return value


class TaskUpdate(BaseModel):

    title: Optional[str] = None

    description: Optional[str] = None

    status: Optional[str] = None

    priority: Optional[
        Literal[
            "low",
            "medium",
            "high"
        ]
    ] = None

    due_date: Optional[str] = None


class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# AI QUICK ADD
# ==========================================

class QuickAddRequest(BaseModel):

    description: str = Field(
        ...,
        min_length=1
    )

    project_id: int


# ==========================================
# STATISTICS RESPONSE
# ==========================================

class ProjectStats(BaseModel):

    id: int

    name: str

    task_count: int

    pending_count: int = 0

    completed_count: int = 0