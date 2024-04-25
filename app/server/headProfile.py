from app import db
from app import app
from models import User, Announcement

with app.app_context():
    
    def getAnnouncements(user):
        userID = User.query.filter_by(email=user).first().id
        announcements = Announcement.query.filter_by(headID = userID).all()
        return announcements