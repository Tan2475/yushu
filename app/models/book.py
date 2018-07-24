from sqlalchemy import String, Integer, Column
from app.models.base import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=True)
    author = Column(String(30), default="未知")
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(Integer, nullable=True, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
