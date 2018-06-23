from flask import current_app
from app.libs.httper import Http


class YuShuBook:
    _isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    _keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    @classmethod
    def search_by_isbn(cls, q):
        url = cls._isbn_url.format(q)
        result = Http.get(url)
        return result

    @classmethod 
    def search_by_keyword(cls, q, page):
        url = cls._keyword_url.format(q, current_app.config["PAGE_COUNT"], cls.calculate_start(page))
        print(url)
        result = Http.get(url)
        return result

    @staticmethod
    def calculate_start(page):
        return (page-1) * current_app.config["PAGE_COUNT"]