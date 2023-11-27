from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .app import Users

class RegisterForm(FlaskForm):

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address is already in use. Please choose a different one.')

    name=StringField(label='Name: ',validators=[Length(min=2,max=30), DataRequired()])
    email=StringField(label='Email: ',validators=[Email(), DataRequired()])
    password1=PasswordField(label='Password: ',validators=[Length(min=6), DataRequired()])
    password2=PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit=SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in!')