from flask import render_template, redirect, flash, url_for, current_app
from flask_login import login_required, current_user

from app.models.base import db
from app.models.gift import Gift
from app.spider.yushu_book import YuShuBook
from app.view_models.drift import MyDrift
from . import web


@web.route("/my/gifts")
@login_required
def my_gifts():
    uid = current_user.id
    # 用于找出当前用户的所有礼物
    gift_of_mine = Gift.get_uer_gifts(uid)
    # 从礼物中获取isbn号
    isbn_list = [gift.isbn for gift in gift_of_mine]
    # 获取到愿望清单对象数组
    wish_count_list = Gift.get_wishs_count(isbn_list)
    # 转换成视图模型
    my_gifts = MyDrift(gift_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=my_gifts.drifts)


@web.route("/gifts/book/<isbn>")
@login_required
def save_to_gifts(isbn):
    yushu = YuShuBook()
    yushu.search_by_isbn(isbn)

    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            db.session.add(gift)
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
    else:
        flash("请勿重复添加已赠送或者正在索要的书籍")
    return redirect(url_for('web.detail', isbn=isbn))


@web.route("/gift/<gid>/redraw")
@login_required
def redraw_from_gifts():
    pass
