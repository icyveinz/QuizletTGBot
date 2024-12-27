import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from controller.mysql_orm_controller.base_init import Base


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_side = Column(String(500), nullable=False)
    reverse_side = Column(String(500), nullable=False)
    user_id = Column(Integer, nullable=False)
    is_studied = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)