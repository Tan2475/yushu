from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, desc, func
from flask import current_app

from app.models.base import Base, db
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    __tablename__ = "gifts"
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
    def recent(cls):
        gift_list = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(Gift.current_time).limit(current_app.config['RECENT_GIFT_COUNT']).distinct().all()
        return gift_list

    @classmethod
    def get_uer_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).all()
        return gifts

    @classmethod
    def get_wishs_count(cls, isbn_list):
        # 查询符合要求的愿望清单，返回包含id和isbn对象的数组
        wish_counts = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 0).group_by(Wish.isbn).all()
        # 序列化原始数据
        wish_count_list = [{"count": w[0], "isbn":w[1]} for w in wish_counts]
        return wish_count_list
