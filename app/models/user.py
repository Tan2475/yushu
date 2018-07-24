from sqlalchemy import Integer, String, Column, Float, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from app.spider.yushu_book import YuShuBook
from .gift import Gift
from .wish import Wish


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    _password = Column('password', String(100))
    gifts = relationship('Gift', backref="user")
    wishs = relationship("Wish", backref="user")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, rwd):
        self._password = generate_password_hash(rwd)

    def check_password(self, rwd):
        return check_password_hash(self._password, rwd)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != "isbn":
            return False
        yushu = YuShuBook()
        yushu.search_by_isbn(isbn)
        if not yushu.firstbook:
            return False
        gifting = Gift.query.filter_by(isbn=isbn, uid=self.id, launched=False).first()
        wishing = Wish.query.filter_by(isbn=isbn, uid=self.id, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))