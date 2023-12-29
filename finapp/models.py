from .database import db

from flask_login import UserMixin
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = mapped_column(String, primary_key=True)
  password = mapped_column(String(128))


class Category(db.Model):
  __tablename__ = 'categories'

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('categories.id'))
  user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey('users.id'))
  hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class Merchant(db.Model):
  __tablename__ = 'merchants'
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey('users.id'))
  hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)
