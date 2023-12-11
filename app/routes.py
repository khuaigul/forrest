 # -*- coding: utf-8 -*-
from app import app
from flask import render_template
from app.forms import LoginForm, SignupForm, NewProfile
from flask import render_template, flash, redirect
from flask import request
from app.server.signup import register, isRegistered, checkSignin

@app.route('/')
def r():
    return "ffg"
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.submit.data, form.signup.data)
        if form.submit.data:
            if checkSignin(form.email.data, form.password.data):
                return redirect('/index')
    if form.signup.data:
            return redirect('/signup')
    return render_template('login.html', title='Sign In', form=form)    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.submit.data:
            if isRegistered(form.email.data):
                return render_template('signup.html', note="Эта почта уже зарегестрирована", form = form)
            if form.password.data != form.passwordRe.data:
                return render_template('signup.html', note="Пароли не совпадают", form = form)
            else:
                register(form.email.data, form.password.data)
                return render_template('signup.html', note="Ссылка с подтверждением отправлена вам на почту", form = form)
    else:
        return render_template('signup.html', note="Введена несуществующая почта", form = form)

@app.route('/newProfile', methods=['GET', 'POST'])
def newProfile():
    form = NewProfile()
    if form.validate_on_submit():
        if form.submit.data:
            print(form.category, form.sport, form.dateOfBirth, form.name, form.gender, form.info)
    return render_template('newProfile.html', form = form)