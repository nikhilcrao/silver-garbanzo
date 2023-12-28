from .database import db

from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = mapped_column(String, primary_key=True)
  password = mapped_column(String(128))


class Category(db.Model):
  __tablename__ = 'categories'
  
  slug: Mapped[str] = mapped_column(String, primary_key=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  parent_slug: Mapped[str] = mapped_column(String, ForeignKey('categories.slug'))

