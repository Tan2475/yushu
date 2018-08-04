from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, func

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    __tablename__ = "wishs"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu = YuShuBook()
        yushu.search_by_isbn(self.isbn)
        return yushu.firstbook

    @classmethod
    def get_user_wish(cls, uid):
        user_wishes = Wish.query.filter_by(launched=False, uid=uid).all()
        return user_wishes

    @classmethod
    def get_gift_count(cls, isbn_list):
        from app.models.gift import Gift
        gift_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False, Gift.status == 0, Gift.isbn.in_(isbn_list)).group_by(Gift.isbn).all()
        gifts = [{"count": g[0], "isbn": g[1]} for g in gift_list]
        return gifts


