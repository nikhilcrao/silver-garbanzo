import os
import datetime

from .database import db
from .forms import RecordAddEditForm, RecordDeleteForm, RecordUploadForm
from .models import Merchant, User, Category, Record
from .category import get_category_id_choices
from .merchant import get_merchant_id_choices
from .recordparser import ImportRecords

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename


bp = Blueprint('record', __name__, url_prefix='/record')


def import_transactions(filename):
  records = ImportRecords(filename)
  for record_dict in records:
    record = Record(
      user_id=current_user.id,
      amount=record_dict['amount'],
      date=datetime.datetime.strptime(record_dict['date'], '%Y-%m-%d %H:%M:%S'),
      description=record_dict['merchant'],
      hash=str(hash(record_dict['merchant'] + str(record_dict['amount']) + str(record_dict['date']))),
    )
    db.session.add(record)
  db.session.commit()
  return len(records)


@bp.route('/')
@login_required
def index():
  records = Record.query.filter_by(user_id=current_user.id).order_by('id').all()
  return render_template('record/index.html', records=records)


@bp.route('/add' , methods=['GET', 'POST'])
@login_required
def add():
  form = RecordAddEditForm(user_id=current_user.id)
  form.category_id.choices = get_category_id_choices()
  form.merchant_id.choices = get_merchant_id_choices()
  
  if form.validate_on_submit():
    record = Record()
    form.populate_obj(record)

    try:      
      db.session.add(record)
      db.session.commit()
      flash(f"Record {form.id.data} added successfully.")
      return redirect(url_for('record.index'))
    except:
      flash(f"Record {form.id.data} could not be added.", 'danger')
      db.session.rollback()
    
  return render_template('record/add.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  record = Record.query.get_or_404(id)
  form = RecordAddEditForm(obj=record)
  form.category_id.choices = get_category_id_choices()
  form.merchant_id.choices = get_merchant_id_choices()

  if form.validate_on_submit():
    form.populate_obj(record)
    try:
      db.session.commit()
      flash(f"Record {form.id.data} updated successfully.")
      return redirect(url_for('record.index'))
    except:
      flash(f"Error updating rule {form.id.data}", 'danger')

  return render_template('record/edit.html', form=form)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  record = Record.query.get_or_404(id)
  form = RecordDeleteForm(obj=record)

  if form.validate_on_submit():
    try:
      db.session.delete(record)
      db.session.commit()
      flash(f"Record {record.id} deleted successfully.")
      return redirect(url_for('record.index'))
    except:
      flash(f"Error deleting record {record.id}", 'danger')
      db.session.rollback()

  return render_template('record/delete.html', record=record, form=form)


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
  form = RecordUploadForm()

  if form.validate_on_submit():
    file = request.files['files']
    if file.filename == '':
      flash('No file selected', 'danger')
      return redirect(url_for('record.upload'))
    if file:
      filename = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        secure_filename(file.filename))
      file.save(filename)
      try:
        count = import_transactions(filename)
        flash(f"Successfully imported {count} records.")        
        return redirect(url_for('record.index'))
      except:
        raise
        flash(f"Error importing transactions: {err}", 'danger')

  return render_template('record/upload.html', form=form)