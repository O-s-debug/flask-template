from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email

class LoginForm(FlaskForm):
    phone = StringField("Phone", validators=[DataRequired(), Regexp(r'^\d{10}$', message="Enter a valid 10-digit number")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    phone = StringField("Phone", validators=[DataRequired(), Regexp(r'^\d{10}$', message="Enter a valid 10-digit number")])
    email = StringField("Email", validators=[DataRequired(), Email(message="Enter a valid email address")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class PredictForm(FlaskForm):
    text = TextAreaField("Input Text", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Predict")

class ForgotPasswordForm(FlaskForm):
    phone = StringField("Phone", validators=[DataRequired(), Regexp(r'^\d{10}$', message="Enter a valid 10-digit number")])
    submit = SubmitField("Send Recovery Code")

class ResetPasswordForm(FlaskForm):
    code = StringField("Recovery Code", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Reset Password")
