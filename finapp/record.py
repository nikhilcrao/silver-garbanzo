import os
import datetime

from .database import db
from .forms import RecordAddEditForm, RecordDeleteForm, RecordUploadForm, RecordSearchForm
from .models import Merchant, User, Category, Record
from .category import get_category_id_choices
from .merchant import get_merchant_id_choices
from .recordparser import ImportRecords

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user, login_required
from sqlalchemy import desc
from werkzeug.utils import secure_filename



csrf = CSRFProtect()


bp = Blueprint('record', __name__, url_prefix='/record')


def import_transactions(filename, type, user_id=None):
  records = ImportRecords(filename, type)
  record_user_id = user_id if user_id else current_user.id
  for record_dict in records:
    record = Record(
      user_id=record_user_id,
      amount=record_dict['amount'],
      date=datetime.datetime.strptime(record_dict['date'], '%Y-%m-%d %H:%M:%S'),
      description=record_dict['merchant'],
      hash=str(hash(record_dict['merchant'] + str(record_dict['amount']) + str(record_dict['date']))),
      category_id=0,
      merchant_id=0,
    )
    db.session.add(record)
  db.session.commit()
  return len(records)


def parse_search_term(term, records):
  tokens = term.split()

  sort_by = ''
  desc_filter = []
  
  for token in tokens:
    if token.startswith('category_id:'):
      category_id = int(token.split(':')[1])
      records = records.filter(Record.category_id == category_id)
    elif token.startswith('merchant_id:'):
      merchant_id = int(token.split(':')[1])
      records = records.filter(Record.merchant_id == merchant_id)
    elif token.startswith('date_from:'):
      date_from = datetime.datetime.strptime(token.split(':')[1], '%Y-%m-%d')
      records = records.filter(Record.date >= date_from)
    elif token.startswith('date_to:'):
      date_to = datetime.datetime.strptime(token.split(':')[1], '%Y-%m-%d')
      records = records.filter(Record.date <= date_to)
    elif token.startswith('sort:'):
      sort_by = token.split(':')[1]
      if token.endswith(',desc'):
        sort_by = desc(sort_by.split(',')[0])
    else:
      desc_filter.append(token)
      
  if len(desc_filter) > 0:
    records = records.filter(
      Record.description.ilike('%' + ' '.join(desc_filter) + '%'))

  if sort_by != '':
    records = records.order_by(sort_by)
  
  return records


@bp.route('/')
@login_required
@csrf.exempt
def index():
  records = db.session.query(Record).filter_by(user_id=current_user.id)
  args = {}

  form = RecordSearchForm()
  if 'search' in request.args:
    form.search.data = request.args['search']
    records = parse_search_term(request.args['search'], records)

  page = request.args.get('page', 1, type=int)
  records = records.paginate(page=page, per_page=50)

  return render_template('record/index.html', records=records, form=form, Record=Record)


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
        count = import_transactions(filename, request.form['type'])
        flash(f"Successfully imported {count} records.")        
        return redirect(url_for('record.index'))
      except:
        raise
        flash(f"Error importing transactions: {err}", 'danger')

  return render_template('record/upload.html', form=form)