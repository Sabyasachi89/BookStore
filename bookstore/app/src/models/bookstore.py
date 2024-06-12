from sqlalchemy import Column, String, Integer
from app.src.database import Base


class BookStore(Base):
    __tablename__ = 't_bookstore'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    description = Column(String)
