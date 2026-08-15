import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# DATABASE URL
# ==========================================

DATABASE_URL="postgresql://postgres.mxmahkakuewukxtboayi:dheeraj%40123@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")


# ==========================================
# DATABASE ENGINE
# ==========================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ==========================================
# DATABASE SESSION
# ==========================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==========================================
# BASE
# ==========================================

Base = declarative_base()


# ==========================================
# DATABASE DEPENDENCY
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()