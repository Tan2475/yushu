def call():
    print("my name is call")


def log(fun):
    def wrapper(*args, **kw):
        print("fun name is %s" %fun.__name__)
        return fun(*args, **kw)
    return wrapper

@log
def call():
    print("my name is call")


call()

# call = log(call)()
# call = wrapper()
# call = print()=> call()
