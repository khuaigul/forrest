from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, FieldList, FormField, SelectMultipleField
from wtforms.validators import Optional, DataRequired, email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.server.cathegories import categoryCountList
from models import Category
from wtforms_alchemy import QuerySelectMultipleField
from flask_appbuilder.fieldwidgets import Select2ManyWidget
from app.server.cathegories import getCategories, getAllCategories
from app.validators.form_validators import BirthdayValidator, passwordValidator, DateNotLessThanToday
# from app import photos

class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(message="Введите почту")])
    password = PasswordField('Password', validators=[DataRequired(message="Введите пароль")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Войти')
    signup = SubmitField('Зарегистрироваться')

class SignupForm(FlaskForm):
    email = StringField('Имя пользователя', validators=[DataRequired(message="Введите пароль")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Введите пароль"), passwordValidator])
    passwordRe = PasswordField('Повторите пароль', validators=[DataRequired(message="Введите пароль")])
    submit = SubmitField('Зарегестрироваться')


class NewProfile(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(message="Это поле обязательное")])
    dateOfBirth = DateField('Дата рождения', validators=[DataRequired(message="Это поле обязательное"), BirthdayValidator])
    gender = SelectField('Пол', coerce=str, choices=['женский', 'мужской'], validators=[DataRequired(message="Это поле обязательное")])
    info = StringField('О себе', validators=[DataRequired(message="Это поле обязательное")])
    categoriesTracking = SelectField('Пеший опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesWater = SelectField('Водный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesSkis = SelectField('Лыжный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesMounts = SelectField('Горный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesBike = SelectField('Велосипедный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesMixed = SelectField('Смешанный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    submit = SubmitField('Зарегестрироваться')
    delete = SubmitField('Отмена')
    saveChanges = SubmitField('Сохранить изменения')

class EditProfile(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(message="Это поле обязательное")])
    dateOfBirth = DateField('Дата рождения', validators=[DataRequired(message="Это поле обязательное")])
    gender = SelectField('Пол', coerce=str, choices=['женский', 'мужской'], validators=[DataRequired(message="Это поле обязательное")])
    info = StringField('О себе', validators=[DataRequired(message="Это поле обязательное")])
    categoriesTracking = SelectField('Пеший опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesWater = SelectField('Водный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesSkis = SelectField('Лыжный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesMounts = SelectField('Горный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesBike = SelectField('Велосипедный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    categoriesMixed = SelectField('Смешанный опыт', coerce=str, choices=categoryCountList(), default=0, validators=[DataRequired(message="Это поле обязательное")])
    saveChanges = SubmitField('Сохранить изменения')

class UploadForm(FlaskForm):
#     photo = FileField(validators=[FileAllowed(photos, 'Разрешены только изображения'), FileRequired('Файл не должен быть пустым')])
    photo = FileField('Документ', validators=[FileRequired(message='Файл не должен быть пустым')])
    submit = SubmitField('Загрузить')
    name = StringField('Введите описание документа', validators=[DataRequired(message="Описание не должно быть пустым")])

class HeadProfile(FlaskForm):
    newTrack = SubmitField('Создать новый поход')

class NewAnnouncement(FlaskForm):
    name = StringField('Название')#, validators=[DataRequired(message="Это поле обязательное")])
    dateBegin = DateField('Дата начала')#, validators=[DataRequired(message="Это поле обязательное")])
    dateEnd = DateField('Дата окончания')#, validators=[DataRequired(message="Это поле обязательное")])
    dateTillOpen = DateField('Дата окончания набора')#, validators=[DataRequired(message="Это поле обязательное")])
    map = StringField('Ссылка на маршрут')
    info = TextAreaField('Информация о походе')
    category = SelectField('Категория похода', coerce=str, choices=getAllCategories())
    submit = SubmitField('Опубликовать')
# class Profile(FlaskForm):
#     name = 
    
class AnnouncementForm(FlaskForm):
    submit = SubmitField('Стать участником')

class AnnouncementConfirm(FlaskForm):
    submit = SubmitField('Да')
    cancel = SubmitField('Назад')

class AnswerRequest(FlaskForm):
    accept = SubmitField('Да')
    decline = SubmitField('Да')
    id = StringField('Идентификатор')
    cancel = SubmitField('Назад')

class MessageForm(FlaskForm):
    send = SubmitField('Отправить')
    text = TextAreaField()

class SearchForm(FlaskForm):
    submit = SubmitField('Поиск')
    text = StringField()
    water = BooleanField('Водный')
    bike = BooleanField('Велосипедный')
    tracking = BooleanField('Пешеходный')
    skis = BooleanField('Лыжный')
    mounts = BooleanField('Горный')
    mixed = BooleanField('Смешанный')
    
    pvd = BooleanField('Поход выходного дня')
    nonsport = BooleanField('Неспортиыный поход')
    category1 = BooleanField('1 к. с.')
    category2 = BooleanField('2 к. с.')
    category3 = BooleanField('3 к. с.')
    category4 = BooleanField('4 к. с.')
    category5 = BooleanField('5 к. с.')
    category6 = BooleanField('6 к. с.')

    dateBegin = DateField('Поход начнётся не раньше', validators=[Optional(), DateNotLessThanToday])
    dateEnd = DateField('Поход закончится не позже', validators=[Optional(), DateNotLessThanToday])

class UserPage(FlaskForm):
    submit = SubmitField("Руководство")