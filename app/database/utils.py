from sqlalchemy.orm import Session
from .session import SessionLocal  # Import SessionLocal from session.py


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
