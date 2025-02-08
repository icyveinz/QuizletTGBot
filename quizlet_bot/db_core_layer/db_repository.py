from typing import Type
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase
from db_core_layer.db_config import SessionLocal, Base


def create_tables(engine: Engine):
    """Create tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a session to interact with the database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
