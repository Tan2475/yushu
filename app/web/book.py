import json
from flask import jsonify, request, render_template, url_for, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web
from app.forms.book import SearchForms


@web.route("/book/search/")
def search():
    forms = SearchForms(request.args)
    books = BookCollection()

    if forms.validate():
        q = forms.q.data.strip()
        page = forms.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == "isbn":
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)
        books.fill(yushu_book, q)
    else:
        flash("很抱歉没有找到您想要的结果")
    
    return render_template("search_book.html", books=books)


@web.route("/book/<isbn>/detail")
def detail(isbn):
    has_in_gifts = False
    has_in_wishs = False

    if current_user.is_authenticated:
        if Gift.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first():
            has_in_wishs = True

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    bookdetail = BookViewModel(yushu_book.firstbook)

    trade_gift = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wish = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_wish_gift = TradeInfo(trade_gift)
    trade_wish_wish = TradeInfo(trade_wish)
    return render_template("book_detail.html", book=bookdetail, gifts=trade_wish_gift, wishs=trade_wish_wish,
                           has_in_gifts=has_in_gifts, has_in_wishs=has_in_wishs)



