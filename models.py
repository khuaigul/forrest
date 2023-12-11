
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
        backref=db.backref('UserPosts', lazy='dynamic'))

    def __init__(self, email, name, dateOfBirth, gender, info):
        self.name = name
        self.email = email
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.info = info
        

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sportStatus = db.Column(db.String(80))
    sportType = db.Column(db.String(80))
    category = db.Column(db.Integer)

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
        backref=db.backref('categoryPosts', lazy='dynamic'))
    
    headID = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile = db.relationship('Profile', backref=db.backref('profilePosts', lazy='dynamic'))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

    announcementID = db.Column(db.Integer, db.ForeignKey('announcement.id'))
    announcement = db.relationship('Announcement', backref=db.backref('announcementPosts', lazy='dynamic'))

# class Message(db.Model):


# db.create_all()