from .database import db
from .forms import RuleAddEditForm, RuleDeleteForm, RuleApplyForm
from .models import Merchant, User, Category, Rule, Record
from .category import get_category_id_choices
from .merchant import get_merchant_id_choices

from flask import Blueprint, render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required


bp = Blueprint('rule', __name__, url_prefix='/rule')


def add_merchant(name):
  merchant = Merchant()
  merchant.name = name
  merchant.user_id = current_user.id
  merchant.hash = str(hash(name + current_user.id))
  
  try:
    db.session.add(merchant)
    db.session.commit()
  except:
    flash(f"Error adding merchant {name}", 'danger')
    db.session.rollback()
    raise
    
  return merchant.id


def add_category(name):
  category = Category()
  category.name = name
  category.user_id = current_user.id
  category.hash = str(hash(name + current_user.id))
  
  try:
    db.session.add(category)
    db.session.commit()
  except:
    flash(f"Error adding category {name}", 'danger')
    db.session.rollback()
    raise
    
  return category.id
  

@bp.route('/')
@login_required
def index():
  rules = Rule.query.filter_by(user_id=current_user.id).order_by('id').all()
  return render_template('rule/index.html', rules=rules, Rule=Rule)


@bp.route('/add' , methods=['GET', 'POST'])
@login_required
def add():
  keywords = ''
  if 'keywords' in request.args:
    keywords = request.args['keywords']

  form = RuleAddEditForm(user_id=current_user.id)
  form.category_id.choices = get_category_id_choices()
  form.merchant_id.choices = get_merchant_id_choices()
  
  if form.validate_on_submit():
    rule = Rule()
    form.populate_obj(rule)

    try:
      print(form.data)
      if form.merchant_id.data == '0' and form.new_merchant_name.data:
        rule.merchant_id = add_merchant(form.new_merchant_name.data)      
      if form.category_id.data == '0' and form.new_category_name.data:
        rule.category_id = add_category(form.new_category_name.data)
      db.session.add(rule)
      db.session.commit()
      flash(f"New rule added successfully.")
      return redirect(url_for('rule.apply'))
    except:
      flash(f"Rule could not be added.", 'danger')
      db.session.rollback()

  form.keywords.data = keywords
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
      print(form.data)
      if form.merchant_id.data == '0' and form.new_merchant_name.data:
        rule.merchant_id = add_merchant(form.new_merchant_name.data)      
      if form.category_id.data == '0' and form.new_category_name.data:
        rule.category_id = add_category(form.new_category_name.data)
      db.session.commit()
      flash(f"Rule {form.id.data} updated successfully.")
      return redirect(url_for('rule.apply'))
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


@bp.route('/apply', methods=['GET', 'POST'])
def apply():
  form = RuleApplyForm()
  rules = Rule.query.filter_by(user_id=current_user.id).order_by('id').all()

  if form.validate_on_submit(): 
    for rule in rules:
      records = Record.query.filter(Record.description.ilike('%' + rule.keywords + '%'))
      for record in records:
        if rule.category_id != 0:
          record.category_id = rule.category_id
        if rule.merchant_id != 0:
          record.merchant_id = rule.merchant_id

    try:
      db.session.commit()
      flash(f"Applied rules successfully.")
      return redirect(url_for('record.index'))
    except:
      flash(f"Error applying rules.", 'danger')
      db.session.rollback()

  return render_template('rule/apply.html', rules=rules, form=form)