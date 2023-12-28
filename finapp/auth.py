from .database import db
from .forms import LoginForm, RegistrationForm
from .models import User

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def init_app(app):
  login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()

  if current_user.is_authenticated:
    return redirect(flask.url_for('index'))

  if form.validate_on_submit():
    hashed_password = generate_password_hash(form.password.data)
    user = User(id=form.username.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account is created. Please login.')
    return redirect(url_for('auth.login'))

  return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if current_user.is_authenticated:
    return redirect(url_for('index'))
  
  if form.validate_on_submit():
    user = User.query.get(form.username.data)
    if user and check_password_hash(user.password, form.password.data):
      login_user(user)
      flash('Logged in successfully.')
      next = request.args.get('next')
      return redirect(next or url_for('index'))
    else:
      flash('Invalid username or password.', 'danger')
    
  return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))