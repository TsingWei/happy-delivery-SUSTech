from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Submit')

class OrderForm(FlaskForm):
    dishID = StringField(validators=[id()])
