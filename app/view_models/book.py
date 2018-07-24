class BookViewModel:
    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.pages = book["pages"] or ""
        self.author = ",".join(book["author"])
        self.price = book["price"]
        self.summary = book["summary"] or ""
        self.image = book["image"]
        self.isbn = book["isbn"]

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return "/".join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ""

    def fill(self, yushu, keyword):
        self.total = yushu.total
        self.books = [BookViewModel(book) for book in yushu.books]
        self.keyword = keyword


