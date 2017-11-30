from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from app import login_manager
from app.form.LoginForm import LoginForm
from app.model import User

home = Blueprint('home', __name__)


@home.route('/')
@login_required
def index():
    # 做些处理
    return render_template('index.html')


@home.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated():
    #     return redirect(url_for('home.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username).first()

        login_user(user, remember=False, force=False, fresh=False)

        # next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return flask.abort(400)

        return redirect(request.args.get('next') or url_for('home.index'))

    return render_template('login.html', form=form)


@home.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()

    return redirect(url_for('home.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
