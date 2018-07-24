from app.models.base import Base
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey


class Wish(Base):
    __tablename__ = "wishs"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

