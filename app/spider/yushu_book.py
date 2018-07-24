from flask import current_app
from app.libs.httper import Http


class YuShuBook:
    _isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    _keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, q):
        url = self._isbn_url.format(q)
        data = Http.get(url)
        self.__package_book_single(data)

    def search_by_keyword(self, q, page):
        url = self._keyword_url.format(q, current_app.config["PAGE_COUNT"], self.calculate_start(page))
        print(url)
        data = Http.get(url)
        self.__package_book_collection(data)

    @staticmethod
    def calculate_start(page):
        return (page-1) * current_app.config["PAGE_COUNT"]

    def __package_book_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __package_book_collection(self, data):
        self.total = data["total"]
        self.books = data["books"]

    @property
    def firstbook(self):
        return self.books[0] if self.books[0] else ""