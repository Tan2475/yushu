from . import web

@web.route("/")
def index():
    return "1"