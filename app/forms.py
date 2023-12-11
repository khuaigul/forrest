from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email
from app.server.cathegories import sportCategories, sportTypes
from models import Category

class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Войти')
    signup = SubmitField('Зарегистрироваться')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    passwordRe = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')

class NewProfile(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    dateOfBirth = DateField('Дата рождения', validators=[DataRequired()])
    gender = SelectField('Пол', coerce=str, choices=['женский', 'мужской'], validators=[DataRequired()])
    info = StringField('О себе', validators=[DataRequired()])
    sport = SelectField('Вид туризма', coerce=str, choices=sportTypes)
    category = SelectField('Категорийный опыт', coerce=int, choices=sportCategories)
    submit = SubmitField('Зарегестрироваться')
    submitCategory = SubmitField('Добавить')