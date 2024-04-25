from app import db
from models import User, Profile, Announcement
from app import app
from datetime import datetime
from app.server.cathegories import getCategoryByID
import random
from app.server.profile import getUserEmail

with app.app_context():
    def createAnnouncement(name, dateBegin, dateEnd, dateTillOpen, map, info, category, username):
        datePost = datetime.today()
        userID = User.query.filter_by(email=username).first().id
        announcement = Announcement(name=name, status="active", info=info, map=map, dateBegin=dateBegin, dateEnd=dateEnd, datePost=datePost, dateTillOpen=dateTillOpen, categoryID=category, headID=userID)
        db.session.add(announcement)
        db.session.commit()
        db.session.close()

    def checkIfHeader(username, announcementID):
        userID = User.query.filter_by(email=username).first().id
        headID = Announcement.query.filter_by(id=announcementID).first().headID
        return userID == headID

    def getAnnouncementsByUser(username):
        changeAnnouncementsStatuses()
        user = User.query.filter_by(email=username).first()
        userID = user.id
        announcements = Announcement.query.filter_by(headID=userID).all()
        result = []
        for announcement in announcements:
            categoryID = announcement.categoryID
            res = (announcement, getCategoryByID(categoryID), user.email, user.id)
            result.append(res)
        return result
    
    def getAnnouncement(id):
        changeAnnouncementStatus(id)
        announcement = Announcement.query.filter_by(id=id).first()
        category = getCategoryByID(announcement.categoryID)
        return [announcement, category]
    
    
    def getRandomAnnouncements(number = 10):
        changeAnnouncementsStatuses()
        announcements = Announcement.query.filter_by(status="active").all()
        records = []
        for announcement in announcements:
            record = announcement
            records.append(record)
        number = min(number, len(records))
        print("DATA", number, len(records))
        records = random.sample(records, number)
        return records
    
    

    def changeAnnouncementStatus(announcementID):
        today = str(datetime.today().strftime('%Y-%m-%d'))
        announcement = Announcement.query.filter_by(id=announcementID).first()
        if today > str(announcement.dateEnd):
            announcement.status = "passed"
        elif today > str(announcement.dateTillOpen):
            announcement.status = "closed"
        db.session.commit()
        db.session.close()

    def changeAnnouncementsStatuses():
        today = str(datetime.today().strftime('%Y-%m-%d'))
        announcements = Announcement.query.all()
        for announcement in announcements:
            # changeAnnouncementStatus(announcement.id)
            if today > str(announcement.dateEnd):
                announcement.status = "passed"
            elif today > str(announcement.dateTillOpen):
                announcement.status = "closed"
        db.session.commit()
        db.session.expunge_all()
        db.session.close()

    def getAnnouncementsByFilters(categories, dateBegin = None, dateEnd = None):
        announcementsIDS = []
        changeAnnouncementsStatuses()
        for category in categories:
            currentAnnouncements = Announcement.query.filter_by(categoryID=category).all()
            for announcement in currentAnnouncements:
                if not dateBegin == None:
                    if str(announcement.dateBegin) < str(dateBegin):
                        continue
                if not dateEnd == None:
                    if str(announcement.dateEnd) > str(dateEnd):
                        continue
                announcementsIDS.append(announcement.id)
        return announcementsIDS
    
    def checkAnnouncementDates(dateBegin, dateEnd, dateTillEnd):
        if dateBegin >= dateEnd:
            return "Дата начала похода не может быть позже даты окончания"
        if dateTillEnd > dateBegin:
            return "Дата окончания набора в поход не может быть позже начала похода"
        return None
    
    