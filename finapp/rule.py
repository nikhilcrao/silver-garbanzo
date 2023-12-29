from .database import db
from .forms import RuleAddEditForm, RuleDeleteForm
from .models import Merchant, User, Category, Rule
from .category import get_category_id_choices
from .merchant import get_merchant_id_choices

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required


bp = Blueprint('rule', __name__, url_prefix='/rule')


@bp.route('/')
@login_required
def index():
  rules = Rule.query.filter_by(user_id=current_user.id).order_by('id').all()
  return render_template('rule/index.html', rules=rules)


@bp.route('/add' , methods=['GET', 'POST'])
@login_required
def add():
  form = RuleAddEditForm(user_id=current_user.id)
  form.category_id.choices = get_category_id_choices()
  form.merchant_id.choices = get_merchant_id_choices()
  
  if form.validate_on_submit():
    rule = Rule()
    form.populate_obj(rule)

    try:      
      db.session.add(rule)
      db.session.commit()
      flash(f"Rule {form.id.data} added successfully.")
      return redirect(url_for('rule.index'))
    except:
      flash(f"Rule {form.id.data} could not be added.", 'danger')
      db.session.rollback()
    
  return render_template('rule/add.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  rule = Rule.query.get_or_404(id)
  form = RuleAddEditForm(obj=rule)
  form.category_id.choices = get_category_id_choices()
  form.merchant_id.choices = get_merchant_id_choices()

  if form.validate_on_submit():
    form.populate_obj(rule)
    try:
      db.session.commit()
      flash(f"Rule {form.id.data} updated successfully.")
      return redirect(url_for('rule.index'))
    except:
      flash(f"Error updating rule {form.id.data}", 'danger')

  return render_template('rule/edit.html', form=form)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  rule = Rule.query.get_or_404(id)
  form = RuleDeleteForm(obj=rule)

  if form.validate_on_submit():
    try:
      db.session.delete(rule)
      db.session.commit()
      flash(f"Rule {rule.id} deleted successfully.")
      return redirect(url_for('rule.index'))
    except:
      flash(f"Error deleting rule {rule.id}", 'danger')
      db.session.rollback()

  return render_template('rule/delete.html', rule=rule, form=form)