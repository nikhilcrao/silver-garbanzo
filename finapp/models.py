from .database import db

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Category(db.Model):
  slug: Mapped[str] = mapped_column(String, primary_key=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  parent_slug: Mapped[str] = mapped_column(String, ForeignKey('category.slug'))

