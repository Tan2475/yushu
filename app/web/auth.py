from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user

from app.forms.auth import RegisterForms, LoginForms
from app.models.base import db
from app.models.user import User
from . import web


@web.route("/register", methods=["GET", "POST"])
def register():
    forms = RegisterForms(request.form)
    if request.method == "POST" and forms.validate():
        user = User()
        user.set_attrs(forms.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("web.login"))
    return render_template("auth/register.html", form=forms)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForms(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.login')
            return redirect(next)
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('auth/login.html', form=form)
