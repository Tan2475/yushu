from flask import current_app, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from . import web


@web.route("/my/wish")
@login_required
def my_wish():
    return "get gift "


@web.route("/wish/book/<isbn>")
@login_required
def save_to_wish(isbn):
    yushu = YuShuBook()
    yushu.search_by_isbn(isbn)

    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
    else:
        flash("请勿重复添加已赠送或者正在索要的书籍")
    return redirect(url_for('web.detail', isbn=isbn))