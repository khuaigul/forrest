from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from datetime import datetime

def passwordValidator(form, field):
    if len(field.data) < 8:
        raise ValidationError("Пароль должен содержать не менее 8-ми символов")

def DateNotLessThanToday(form, field):
    print("data", field.data)
    date = str(field.data)
    today = str(datetime.today().strftime('%Y-%m-%d'))
    print(today)
    if date < today or date < "1900-01-01":
        raise ValidationError("Введена некорректная дата")

def BirthdayValidator(form, field):
    date = str(field.data)
    today = str(datetime.today().strftime('%Y-%m-%d'))
    if date > today or date < "1900-01-01":
        raise ValidationError("Введена некорректная дата")
