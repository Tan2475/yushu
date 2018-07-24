from contextlib import contextmanager

@contextmanager
def book_print():
    print("<", end="")
    yield
    print(">", end="")


with book_print():
    print("战锤40k", end="")
