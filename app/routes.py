from app import app
# , photos
from flask import render_template, make_response, url_for, session
from app.forms import UploadForm, SearchForm, MessageForm,  AnswerRequest, AnnouncementConfirm, AnnouncementForm, EditProfile, LoginForm, SignupForm, NewProfile, HeadProfile, NewAnnouncement
from flask import render_template, flash, redirect
from flask import request
from app.server.signup import userExists, register, isRegistered, checkSignin, createProfile, delete, logout
# from werkzeug.datastructures import MultiDict
from app.server.profile import getProfileDocs, getUserUsername, getUserData, getProfileData, updateProfile
from app.server.headProfile import getAnnouncements
from app.server.announcements import checkIfHeader, checkAnnouncementDates,  getAnnouncement, createAnnouncement, getAnnouncementsByUser
from app.server.cathegories import getAllCategories
from models import Profile
from datetime import date
from flask_paginate import Pagination, get_page_args
from app.server.pagination import get_announcements_pag
from app.server.requests import getParticipants, checkIfRequestAllowed, getPassedTravelsByUser, getTravelsByUser, declineRequest, acceptRequest, checkIfHeaderByRequest, changeWatchedStatus, getRequests, newRequest, requestsCount
from app.server.messages import checkIfChatAllowed, makeWathed, sendMessage, getChats, getMessages
from app.server.search import getSearchResult
from app.server.main import getUserRecommendations
from app.server.images import createDocument, getDocNameForUser, allowed_file
import pathlib
import os
# from werkzeug.utils import secure_filename
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('')

@app.before_request
def before_request():
    print(request.path)
    # if request.path == "/static/css/style.css":
    #     pass
    # allowList = ['/login', '/signup']
    # allPages = ['/login', 'signup', '/newProfile' '/', '/main', '/profile', '/newAnnouncement', 'headProfile']
    # if 'user' not in session:
    #     if request.path in allowList:
    #         pass
    #     else:
    #         return redirect('/login')
    # print(request.path)
    # if request.path == '/answerRequest':
    #     args = request.args
    #     id = args.get("id")
    #     username = session["user"]
    #     print(checkIfHeaderByRequest(id, username))
    #     if not checkIfHeaderByRequest(id, username):
    #         return redirect('/')
    #     else:
    #         pass
        
    # if request.path not in allowList:       
    #     profile = Profile.query.filter_by(email=session["user"]).all()
    #     if profile == [] and request.path != '/newProfile' and request.path not in allowList:
    #         print("go to new profile")
    #         return redirect('/newProfile')
    # print('accept')

    



@app.route('/')
def r():
    return redirect('/main')

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("HERE LOGIN")
    form = LoginForm()
    if form.validate_on_submit():
        print("validate")
        if form.submit.data:
            print("HERE")
            if not userExists(form.email.data):
                return render_template('login.html', note= "Пользователя не существует", form=form)
            if checkSignin(form.email.data, form.password.data):
                session['user'] = form.email.data
                return redirect('/main')
            else: 
                print("wrong password")
                return render_template('login.html', note= "Неверный пароль", form=form)
    else:
        print("error validate")
    if form.signup.data:
        return redirect('/signup')
    else:
        print("ERROR")
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
                session['user'] = form.email.data
                register(form.email.data, form.password.data)
                return redirect('/newProfile')
    return render_template('signup.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
def toLofout():
    logout()
    return redirect('/login')

@app.route('/newProfile', methods=['GET', 'POST'])
def newProfile():
    print("HERE NEWPROFILE")
    form = NewProfile()
    if form.validate_on_submit():
        if form.submit.data:
            username = session['user']
            createProfile(username, form.name.data, form.dateOfBirth.data, form.gender.data, form.info.data, form.categoriesTracking.data, form.categoriesWater.data, form.categoriesSkis.data, form.categoriesMounts.data, form.categoriesBike.data, form.categoriesMixed.data)
            session['isProfile'] = True
            return redirect('/main')
    if form.delete.data:
        delete(session['user'])
        logout()
        return redirect('/login')
    print("error")
    return render_template('newProfile.html', form = form)

@app.route('/main', methods=['GET', 'POST'])
def main():
    username = session['user']
    alarmCount =requestsCount(username)
    form = SearchForm()
    
    if form.validate_on_submit():
        if form.submit.data:
            print("SEARCH")
            data = getSearchResult(form.text.data, form.tracking.data, form.water.data, form.mounts.data, form.skis.data, form.bike.data, form.mixed.data, form.pvd.data, form.nonsport.data, form.category1.data, form.category2.data, form.category3.data, form.category4.data, form.category5.data, form.category6.data, form.dateBegin.data, form.dateEnd.data)
            print(data)
            page = request.args.get('page', 1, type=int)
            if page == None or page == 0:
                page = 1
            per_page = 10
            start = (page - 1) * per_page
            end = start + per_page
            total_pages = (len(data) + per_page - 1) // per_page
            if page > total_pages:
                page = total_pages
            data_pag = data[start:end]
            return render_template('main.html', page=page, total_pages=total_pages, form=form, data=data, alarmCount=alarmCount, recomendations = False, username=username, announcements=data_pag)
    else:
        data = getUserRecommendations(username)
        return render_template('main.html', form=form, data=data, alarmCount=alarmCount, username=username, announcements = data, recomendations = True)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session['user']
    alarmCount =requestsCount(username)
    profileData = getProfileData(username)
    profileData['dateOfBirth'] = profileData['dateOfBirth'].strftime('%Y-%m-%d')
    print(profileData['dateOfBirth'])
    # profileData.dateOfBirth = date(profileData.dateOfBirth)
    profileDocs = getProfileDocs(username)
    form = EditProfile()
    

    if form.validate_on_submit():
        print("validated")
        if form.saveChanges.data:
            print("UPDATE PROFILE", form.categoriesMounts.data)
            updateProfile(username, form.name.data, form.dateOfBirth.data, form.gender.data, form.info.data, form.categoriesTracking.data, form.categoriesWater.data, form.categoriesSkis.data, form.categoriesMounts.data, form.categoriesBike.data, form.categoriesMixed.data)
            return redirect('/profile')
    else:
        print("ERRORS")
        print(form.errors)
    return render_template('profile.html', profileDocs = profileDocs, alarmCount=alarmCount,username=username, form=form, data = profileData)

@app.route('/uploadDocs', methods=['GET', 'POST'])
def uploadDocs():
    username = session["user"]
    alarmCount =requestsCount(username)
    form = UploadForm()
    if form.validate_on_submit():
        if form.submit.data:
            file = form.photo.data
            if not allowed_file(file):
                return redirect('/uploadDocs')
            filename = getDocNameForUser(username)
            extention = pathlib.Path(file.filename).suffix
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + extention))
            createDocument(username, filename + extention, form.name.data)
            return redirect('/profile')
    return render_template('uploadDocs.html', form=form, username=username, alarmCount=alarmCount)


@app.route('/user', methods=['GET', 'POST'])
def user():
    username = session['user']
    alarmCount =requestsCount(username)
    args = request.args
    id = args.get("id")
    # if not checkIfUserAllowed(id, username):
    #     return redirect('/')
   
    travels = getPassedTravelsByUser(id)
    data = getUserData(id)
    profileDocs = getProfileDocs(getUserUsername(id))
    return render_template('/user.html', userID=id, profileDocs=profileDocs, data = data, announcements=travels, alarmCount=alarmCount, username=username)

@app.route('/headProfile', methods=['GET', 'POST'])
def headProfile():
    form = HeadProfile()
    username = session['user']
    alarmCount =requestsCount(username)
    announcements = getAnnouncementsByUser(username)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(announcements) + per_page - 1) // per_page
    print(page, total_pages)
    if page > total_pages:
        return redirect('/headProfile?page='+str(total_pages))
    announcements_pag = announcements[start:end]
    print("ANN",announcements_pag)
    if form.validate_on_submit():
        if form.newTrack.data:
            return redirect('/main')
    return render_template('headProfile.html',alarmCount=alarmCount,username=username, form=form, announcements = announcements_pag, total_pages=total_pages, page=page)

@app.route('/travels', methods = ['GET', 'POST'])
def travels():
    username = session['user']
    alarmCount =requestsCount(username)
    announcements = getTravelsByUser(username)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(announcements) + per_page - 1) // per_page
    print(page, total_pages)
    if page > total_pages:
        return redirect('/travels?page='+str(total_pages))
    announcements_pag = announcements[start:end]
    print("ANN",announcements_pag)
    return render_template('travels.html',alarmCount=alarmCount,username=username, announcements = announcements_pag, total_pages=total_pages, page=page)

@app.route('/newAnnouncement', methods=['GET', 'POST'])
def newAnnouncement():
    form = NewAnnouncement()
    username = session['user']
    alarmCount =requestsCount(username)
    
    if form.validate_on_submit():
        if form.submit.data:
            note = checkAnnouncementDates(form.dateBegin.data, form.dateEnd.data, form.dateTillOpen.data)
            if not note == None:
                return render_template('/newAnnouncement.html',alarmCount=alarmCount, username=username, form=form, note=note, noteStatus=True)
            createAnnouncement(form.name.data, form.dateBegin.data, form.dateEnd.data, form.dateTillOpen.data, form.map.data, form.info.data, form.category.data, username)
            return redirect('/headProfile')
    else:
        print('not validated')
        
    return render_template('/newAnnouncement.html',alarmCount=alarmCount, username=username, form=form, noteStatus=False)

@app.route('/announcementConfirm', methods=['GET', 'POST'])
def announcementConfirm():
    form = AnnouncementConfirm()
    username = session['user']
    alarmCount =requestsCount(username)
    args = request.args
    id = args.get("id")
    name, category = getAnnouncement(id)
    name = name.name
    if id == None or checkIfHeader(username, id):
        return redirect('/')
    if form.validate_on_submit():
        if form.submit.data:
            newRequest(username, id)
            return redirect('/announcement?id='+id)
        if form.cancel.data:
            return redirect('/announcement?id='+id)
    return render_template('/announcementConfirm.html',alarmCount=alarmCount, name=name, form=form)


@app.route('/announcement', methods=['GET', 'POST'])
def announcement():
    username = session['user']
    alarmCount = requestsCount(username)
    print("ALARM", alarmCount)
    args = request.args
    id = args.get("id")
    if id == None :
        return redirect('/')
    form = AnnouncementForm()
    if form.validate_on_submit():
        if form.submit.data:
            return redirect('/announcementConfirm?id='+id)
    else:
        print(form.errors)
    info, category = getAnnouncement(id)
    dateBegin = info.dateBegin.strftime('%Y-%m-%d')
    dateEnd = info.dateEnd.strftime('%Y-%m-%d')
    dateTillOpen = info.dateTillOpen.strftime('%Y-%m-%d')
    allowed = checkIfRequestAllowed(id, username)
    return render_template('/announcement.html',alarmCount=alarmCount,dateBegin=dateBegin, dateEnd=dateEnd, dateTillOpen=dateTillOpen, allowed=allowed, username=username, form=form, info=info, category = category) 

@app.route('/notifications', methods=['GET', "POST"])
def notifications():
    username = session['user']
    alarmCount = requestsCount(username)
    requests = getRequests(username)
    print(requests)
    page = request.args.get('page', 1, type=int)
    per_page = 2
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(requests) + per_page - 1) // per_page
    requests_pag = requests[start:end]
    changeWatchedStatus(username)
    return render_template('/notifications.html', alarmCount=alarmCount, username=username, requests = requests_pag, total_pages=total_pages, page=page)

@app.route('/answerRequest', methods=['GET', 'POST'])
def answerRequest():
    username = session['user']
    alarmCount = requestsCount(username)
    args = request.args
    id = args.get("id")
    form = AnswerRequest()
    if form.validate_on_submit():
        if form.accept.data:
            print("ACCEPT BUTTON")
            acceptRequest(id)
            return redirect('/notifications')
        if form.decline.data:
            declineRequest(id)
            return redirect('/notifications')
        if form.cancel.data:
            return redirect('/notifications')
    else:
        print(form.errors)
    return render_template('/answerRequest.html',form=form, alarmCount=alarmCount, id=id, username=username, answer=args.get("answer"), userID=args.get("user"), userName=args.get("username"), announcementName=args.get("announcementName"), announcementID=args.get("announcementID"))

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = session['user']
    alarmCount = requestsCount(username)
    chats = getChats(username)
    args = request.args
    id = args.get("id")
    print("chats", chats)
    if id == None:
        return render_template('/messages.html', alarmCount=alarmCount, username=username, chats=chats, open="False")
    if not checkIfChatAllowed(id, username):
        return render_template('/messages.html', alarmCount=alarmCount, username=username, chats=chats, open="False")
    makeWathed(id, username)
    form = MessageForm()
    messages = getMessages(id)

    print("TYPE", type(chats[0]["id"]), type(id))


    if form.validate_on_submit():
        if form.send.data:
            sendMessage(username, form.text.data, id)
            return redirect('/messages?id='+id)
 
    return render_template('/messages.html', form=form, alarmCount=alarmCount, username=username, chats=chats, open="True", messages=messages, id=int(id))

@app.route('/participants', methods=['GET', 'POST'])
def participants():
    username = session['user']
    alarmCount = requestsCount(username)
    args = request.args
    id = args.get("id")
    participants = getParticipants(id)
    announcement = getAnnouncement(id)[0]
    userIsHeader = checkIfHeader(username, id)
    return render_template('/participants.html', userIsHeader=userIsHeader, alarmCount=alarmCount, announcement=announcement, username=username, participants=participants)
 