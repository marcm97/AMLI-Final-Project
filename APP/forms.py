from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextField
from wtforms.validators import DataRequired,required

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ReusableForm(FlaskForm):
    departure = TextField('deparature', validators=[required()])
    destination = TextField('destination', validators=[required()])
    restaurant = TextField('restaurant', validators=[required()])
    submit = SubmitField('Get new restaurants')