def is_isbn_or_key(q):
    isbn_or_key = "key"
    if len(q) == 13 and q.isdigit():
        isbn_or_key = "isbn"
    short_word = q.replace("-", "")
    if "-" in q and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = "isbn"
    return isbn_or_key 