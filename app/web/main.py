from flask import render_template

from . import web
from app.models.gift import Gift
from ..view_models.book import BookViewModel


@web.route("/")
def index():
    recent = Gift.recent()
    gifts = [BookViewModel(gift.book) for gift in recent]
    return render_template('index.html', recent=gifts)
