from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField


class LoginForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Submit')

class OrderForm(FlaskForm):
    dishID = HiddenField()
    dishname = StringField('dishname')
    add = SubmitField('买')
