from .database import db
from .forms import CategoryAddEditForm, CategoryDeleteForm
from .models import Category, User

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from slugify import slugify
from sqlalchemy import or_


bp = Blueprint('category', __name__, url_prefix='/category')

def get_categories():
  return Category.query.filter(
    or_(
      Category.user_id == current_user.id,
      Category.user_id == None,
    )
  ).order_by('name')


def get_category_id_choices(roots_only=False, exclude_ids=[]):
  categories = get_categories()
  if roots_only:
    categories = categories.filter_by(parent_id=0)
  category_id_choices = [(0, 'None')]
  for category in categories:
    if category.id not in exclude_ids:
      category_id_choices.append((category.id, category.name))
  return category_id_choices


@bp.route('/')
@login_required
def index():
  return render_template('category/index.html', categories=get_categories())


@bp.route('/add' , methods=['GET', 'POST'])
@login_required
def add():
  form = CategoryAddEditForm(user_id=current_user.id)
  form.parent_id.choices = get_category_id_choices(roots_only=True)
  
  if form.validate_on_submit():
    category = Category()
    form.populate_obj(category)
    category.hash = str(hash(form.name.data + form.user_id.data))
    try:      
      db.session.add(category)
      db.session.commit()
      flash(f"Category {form.name.data} added successfully.")
      return redirect(url_for('category.index'))
    except:
      flash(f"Category {form.name.data} could not be added.", 'danger')
      db.session.rollback()
    
  return render_template('category/add.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  category = Category.query.get_or_404(id)
  form = CategoryAddEditForm(obj=category)
  form.parent_id.choices = get_category_id_choices(roots_only=True, exclude_ids=[id])

  if form.validate_on_submit():
    form.populate_obj(category)
    category.hash = str(hash(form.name.data + form.user_id.data))
    try:
      db.session.commit()
      flash(f"Category {form.name.data} updated successfully.")
      return redirect(url_for('category.index'))
    except:
      flash(f"Error updating category {form.name.data}", 'danger')

  return render_template('category/edit.html', form=form)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  category = Category.query.get_or_404(id)
  form = CategoryDeleteForm(obj=category)

  if form.validate_on_submit():
    try:
      db.session.delete(category)
      db.session.commit()
      flash(f"Category {category.name} deleted successfully.")
      return redirect(url_for('category.index'))
    except:
      flash(f"Error deleting category {category.name}", 'danger')
      db.session.rollback()

  return render_template('category/delete.html', category=category, form=form)