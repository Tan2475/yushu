from app.models.base import Base
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey


class Gift(Base):
    __tablename__ = "gifts"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

