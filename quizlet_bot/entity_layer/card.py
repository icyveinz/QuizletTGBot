import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from controller import Base


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    front_side = Column(String(500), nullable=False)
    back_side = Column(String(500), nullable=False)
    user_id = Column(String(50), nullable=False, index=True)
    is_studied = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
