from .database import db
from .forms import MerchantAddEditForm, MerchantDeleteForm
from .models import Merchant, User

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required


bp = Blueprint('merchant', __name__, url_prefix='/merchant')


def get_merchants():
  return Merchant.query.filter_by(user_id=current_user.id).order_by('name')


def get_merchant_id_choices(exclude_ids=[]):
  merchants = get_merchants()
  merchant_id_choices = [(0, 'None')]
  for merchant in merchants:
    if merchant.id not in exclude_ids:
      merchant_id_choices.append((merchant.id, merchant.name))
  return merchant_id_choices
  

@bp.route('/')
@login_required
def index():
  merchants = get_merchants()
  return render_template('merchant/index.html', merchants=merchants)


@bp.route('/add' , methods=['GET', 'POST'])
@login_required
def add():
  form = MerchantAddEditForm(user_id=current_user.id)
  
  if form.validate_on_submit():
    merchant = Merchant()
    form.populate_obj(merchant)
    merchant.hash = str(hash(form.name.data + form.user_id.data))
    try:      
      db.session.add(merchant)
      db.session.commit()
      flash(f"Merchant {form.name.data} added successfully.")
      return redirect(url_for('merchant.index'))
    except:
      flash(f"Merchant {form.name.data} could not be added.", 'danger')
      db.session.rollback()
    
  return render_template('merchant/add.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  merchant = Merchant.query.get_or_404(id)
  form = MerchantAddEditForm(obj=merchant)

  if form.validate_on_submit():
    form.populate_obj(merchant)
    merchant.hash = str(hash(form.name.data + form.user_id.data))
    try:
      db.session.commit()
      flash(f"Merchant {form.name.data} updated successfully.")
      return redirect(url_for('merchant.index'))
    except:
      flash(f"Error updating merchant {form.name.data}", 'danger')

  return render_template('merchant/edit.html', form=form)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  merchant = Merchant.query.get_or_404(id)
  form = MerchantDeleteForm(obj=merchant)

  if form.validate_on_submit():
    try:
      db.session.delete(merchant)
      db.session.commit()
      flash(f"Merchant {merchant.name} deleted successfully.")
      return redirect(url_for('merchant.index'))
    except:
      flash(f"Error deleting merchant {merchant.name}", 'danger')
      db.session.rollback()

  return render_template('merchant/delete.html', merchant=merchant, form=form)