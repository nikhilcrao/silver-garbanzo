import click
import os

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


def init_category(app):
  CATEGORY_DICT = {
    'Income': ['Paycheck', 'Investment', 'Returns', 'Rental', 'Reimbursement'],
    'Entertainment': ['Arts', 'Music', 'Movies', 'Subscriptions'],
    'Shopping': ['Clothing', 'Books', 'Electronics', 'Hobbies', 'Sporting Goods'],
    'Health & Fitness': ['Doctor', 'Dentist', 'Eye Care', 'Pharmacy', 'Health Insurance', 'Gym', 'Sports'],
    'Food & Dining': ['Groceries', 'Snacks & Sweets', 'Restaurants', 'Alcohol'],
    'Investments': ['Deposit', 'Withdrawal', 'Dividend'],
    'Auto & Transport': ['Fuel & EV', 'Parking', 'Service & Auto Parts', 'Auto Loan', 'Auto Insurance', 'Driver'],
    'Fees & Charges': ['Foreign Currency Fees', 'Service Fees'],
    'Uncategorized': ['Cash & ATM', 'Check', 'Other'],
    'Kids': ['Tuition', 'Activities & Classes', 'Toys & Games', 'School Supplies'],
    'Personal Care': ['Hair', 'Spa & Massage', 'Laundry'],
    'Gifts & Donations': ['Gift', 'Charity'],
    'Bills & Utilities': ['Mobile Phone', 'Internet', 'Electricity', 'Water', 'Gas'],
    'Travel': ['Air Travel', 'Hotel', 'Rental & Taxi', 'Vacation'],
    'Home': ['Maid', 'Gardener', 'Cook', 'Cleaning', 'Rent', 'Mortgage'],
    'Transfer': ['Credit Card Payment', 'Account Transfer'],
  }
  from .models import Category
  with app.app_context():
    for parent_category_name in CATEGORY_DICT:
      category = Category()
      category.name = parent_category_name
      category.user_id = None
      category.parent_id = 0
      category.hash = str(hash(category.name + str(category.user_id)))
      db.session.add(category)
      db.session.commit()
      parent_category_id = category.id

      for child_category_name in CATEGORY_DICT[parent_category_name]:
        category = Category()
        category.name = child_category_name
        category.user_id = None
        category.hash = str(hash(category.name + str(category.user_id)))
        category.parent_id = parent_category_id
        db.session.add(category)
        
      db.session.commit()
  print('Init category')


def init_records(app):
  from .record import import_transactions
  for file in os.listdir(app.config['UPLOAD_FOLDER']):
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file)
    count = -1
    if filename.endswith('.csv'):
      count = import_transactions(filename, 'cc', user_id='nikhilcrao')
    elif filename.endswith('.txt'):
      count = import_transactions(filename, 'acct', user_id='nikhilcrao')
    print(f"Imported {count} records from {filename}")
      