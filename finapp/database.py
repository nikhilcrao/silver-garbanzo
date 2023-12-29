import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
  db.init_app(app)
  init_db(app)


def init_db(app):
  from . import models
  with app.app_context():
    db.create_all()


def reset_db(app):
  from . import models
  with app.app_context():
    db.drop_all()
    db.create_all()
    print('Database reset.')