from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from flask import jsonify, request
from . import web
from app.forms.book import SearchForms


@web.route("/book/search/")
def search():
    forms = SearchForms(request.args)
    if forms.validate():
        q = forms.q.data.strip()
        page = forms.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == "isbn":
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page)
        return jsonify(result), 200
