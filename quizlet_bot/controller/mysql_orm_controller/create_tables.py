from typing import Type

from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase


def create_tables(engine : Engine, Base : Type[DeclarativeBase]):
    Base.metadata.create_all(bind=engine)