from flask_wtf import FlaskForm
from wtforms import (
  StringField, PasswordField, SubmitField, HiddenField, SelectField, IntegerField
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