from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextField
from wtforms.validators import DataRequired,required


class ReusableForm(FlaskForm):
    departure = TextField('deparature', validators=[required()])
    destination = TextField('destination', validators=[required()])
    restaurant = TextField('restaurant', validators=[required()])
    submit = SubmitField('Get new restaurants')