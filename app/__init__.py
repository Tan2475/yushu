from flask import Flask
from flask_login import LoginManager

from app.models.base import db

login_manager = LoginManager()
from app.models import user, gift, wish, book

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.secure")
    app.config.from_object("app.setting")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    with app.app_context():
        db.create_all()

    from app.web import web
    app.register_blueprint(web)
    return app





