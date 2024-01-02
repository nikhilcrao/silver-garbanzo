from flask_wtf import FlaskForm
from wtforms import (
  StringField, PasswordField, SubmitField, HiddenField, SelectField, IntegerField, FloatField, DateTimeField, FileField
)
from wtforms.validators import Optional
from wtforms.widgets import HiddenInput


class LoginForm(FlaskForm):
  username = StringField('Username')
  password = PasswordField('Password')
  submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
  username = StringField('Username')
  password = PasswordField('Password')
  submit = SubmitField('Submit')


class CategoryAddEditForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  user_id = HiddenField(validators=[Optional()])
  name = StringField('Name')
  parent_id = SelectField('Parent Category')
  submit = SubmitField('Submit')
  hash = HiddenField(validators=[Optional()])


class CategoryDeleteForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  submit = SubmitField('Submit')


class MerchantAddEditForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  user_id = HiddenField(validators=[Optional()])
  name = StringField('Name')
  submit = SubmitField('Submit')
  hash = HiddenField(validators=[Optional()])


class MerchantDeleteForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  submit = SubmitField('Submit')


class RuleAddEditForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  user_id = HiddenField(validators=[Optional()])
  keywords = StringField('Keywords')
  merchant_id = SelectField('[Existing] Merchant', validators=[Optional()])
  new_merchant_name = StringField('[New] Merchant Name', validators=[Optional()])
  category_id = SelectField('Category', validators=[Optional()])
  new_category_name = StringField('New Category Name', validators=[Optional()])
  submit = SubmitField('Submit')


class RuleDeleteForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  submit = SubmitField('Submit')


class RuleApplyForm(FlaskForm):
  submit = SubmitField('Submit')


class RecordAddEditForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  hash = HiddenField(validators=[Optional()])
  user_id = HiddenField(validators=[Optional()])
  description = StringField('Description')
  notes = StringField('Notes')
  amount = FloatField('Amount')
  date = DateTimeField('Datetime')
  merchant_id = SelectField('Merchant')
  category_id = SelectField('Category')
  submit = SubmitField('Submit')


class RecordDeleteForm(FlaskForm):
  id = IntegerField(label='', validators=[Optional()], widget=HiddenInput())
  submit = SubmitField('Submit')


class RecordUploadForm(FlaskForm):
  files = FileField('File')
  submit = SubmitField('Submit')


class RecordSearchForm(FlaskForm):
  search = StringField('Search')
  submit = SubmitField('Search')