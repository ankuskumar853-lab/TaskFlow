from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from pwdlib import PasswordHash
from jose import jwt

import models
import schemas

from database import get_db


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ==========================================
# PASSWORD HASHER
# ==========================================

password_hash = PasswordHash.recommended()


# ==========================================
# JWT CONFIGURATION
# ==========================================

SECRET_KEY = "taskflow-secret-key-change-this"
ALGORITHM = "HS256"


# ==========================================
# CREATE USER / REGISTER
# ==========================================

@router.post(
    "/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # --------------------------------------
    # CHECK EXISTING EMAIL
    # --------------------------------------

    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email == user.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    # --------------------------------------
    # HASH PASSWORD
    # --------------------------------------

    hashed_password = password_hash.hash(
        user.password
    )


    # --------------------------------------
    # CREATE USER
    # --------------------------------------

    new_user = models.User(

        name=user.name,

        email=user.email,

        password_hash=hashed_password

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user


# ==========================================
# GET ALL USERS
# ==========================================

@router.get(
    "/",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    return db.query(
        models.User
    ).all()


# ==========================================
# LOGIN
# ==========================================

@router.post(
    "/login",
    response_model=schemas.TokenResponse
)
def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------
    # FIND USER
    # --------------------------------------

    user = (
        db.query(models.User)
        .filter(
            models.User.email == login_data.email
        )
        .first()
    )


    # --------------------------------------
    # CHECK USER
    # --------------------------------------

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    # --------------------------------------
    # CHECK PASSWORD
    # --------------------------------------

    if not user.password_hash:

        raise HTTPException(
            status_code=401,
            detail=(
                "This account does not have "
                "a password. Please register again "
                "or create a new account."
            )
        )


    valid_password = password_hash.verify(
        login_data.password,
        user.password_hash
    )


    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    # --------------------------------------
    # CREATE JWT TOKEN
    # --------------------------------------

    token_data = {

        "sub": str(user.id),

        "email": user.email

    }


    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return {

        "access_token": access_token,

        "token_type": "bearer"

    }