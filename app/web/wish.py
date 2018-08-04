from flask import current_app, url_for, flash, render_template, redirect
from flask_login import login_required, current_user

from app.models.base import db
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from . import web
from app.view_models.drift import MyDrift


@web.route("/my/wish")
@login_required
def my_wish():
    uid = current_user.id
    wish_of_mine = Wish.get_user_wish(uid)
    isbn_list = [wish.isbn for wish in wish_of_mine]
    gift_count_list = Wish.get_gift_count(isbn_list)
    my_wishes = MyDrift(wish_of_mine, gift_count_list)
    return render_template("my_wishes.html", wishes=my_wishes.drifts)


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


