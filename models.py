
import os
from flask import Flask, render_template, request, url_for, redirect

from sqlalchemy.sql import func
 
 
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    name = db.Column(db.String(80))
    dateOfBirth = db.Column(db.DateTime)
    gender = db.Column(db.String(5))
    info = db.Column(db.String(200))

    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('profile', lazy='dynamic'))

    # def __init__(self, email, name, dateOfBirth, gender, info):
    #     self.name = name
    #     self.email = email
    #     self.dateOfBirth = dateOfBirth
    #     self.gender = gender
    #     self.info = info
        

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sportStatus = db.Column(db.String(80))
    sportType = db.Column(db.String(80))
    category = db.Column(db.Integer)

    # def __str__(self):
    #     return self.sportType

    # def __init__(self, sportStatus, sportType, category):
    #     self.sportStatus = sportStatus
    #     self.sportType = sportType
    #     self.category = category

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    status = db.Column(db.String(80))
    info = db.Column(db.String(80))
    map = db.Column(db.String(80))
    dateBegin = db.Column(db.DateTime)
    dateEnd = db.Column(db.DateTime)
    datePost = db.Column(db.DateTime)
    dateTillOpen = db.Column(db.DateTime)

    categoryID = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('categoryAnnouncement', lazy='dynamic'))
    
    headID = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile = db.relationship('User', backref=db.backref('userAnnouncement', lazy='dynamic'))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(80))
    watchedStatus = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('userRequest', lazy='dynamic'))

    announcementID = db.Column(db.Integer, db.ForeignKey('announcement.id'))
    announcement = db.relationship('Announcement', backref=db.backref('announcementRequest', lazy='dynamic'))



class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    text = db.Column(db.String(2000))

    firstUserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstUser = db.relationship('User', foreign_keys=[firstUserID], backref=db.backref('firstUserMessage', lazy='dynamic'))

    secondUserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    secondUser = db.relationship('User', foreign_keys=[secondUserID], backref=db.backref('secondUserMessage', lazy='dynamic'))

    status = db.Column(db.String(80))
    sendTime = db.Column(db.DateTime())

    chatID = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat', backref=db.backref('message', lazy='dynamic'))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    firstUserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstUser = db.relationship('User', foreign_keys=[firstUserID], backref=db.backref('firstUserChat', lazy='dynamic'))

    secondUserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    secondUser = db.relationship('User', foreign_keys=[secondUserID], backref=db.backref('secondUserChat', lazy='dynamic'))

    status = db.Column(db.String(80))



class UserSkill(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   
   userID = db.Column(db.Integer, db.ForeignKey('user.id'))
   user = db.relationship('User', backref=db.backref('userSkill', lazy='dynamic'))

   categoryID = db.Column(db.Integer, db.ForeignKey('category.id'))
   category = db.relationship('Category', backref=db.backref('userSkill', lazy='dynamic'))

class UserHeadSkill(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   
   userID = db.Column(db.Integer, db.ForeignKey('user.id'))
   user = db.relationship('User', backref=db.backref('userHeadSkill', lazy='dynamic'))

   categoryID = db.Column(db.Integer, db.ForeignKey('category.id'))
   category = db.relationship('Category', backref=db.backref('userHeadSkill', lazy='dynamic'))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user', lazy='dynamic'))
    filename = db.Column(db.String(200))
    name = db.Column(db.String(200))
    # extention = db.Column(db.String(20))


# db.create_all()