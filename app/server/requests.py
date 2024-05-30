from models import User, Request, Announcement, Profile
from app import app, db
from datetime import datetime
from app.server.profile import getUserName, getUserEmail
from app.server.messages import makeChat
from app.server.cathegories import getCategoryByID
from app.server.announcements import changeAnnouncementsStatuses

with app.app_context():
    def newRequest(username, id):
        userID = User.query.filter_by(email=username).first().id
        req = Request(watchedStatus="notWatched", status = "waiting", date=datetime.now(), userID=userID, announcementID=id)
        db.session.add(req)
        db.session.commit()
        db.session.close()

    def checkIfRequestAllowed(id, username):
        announcement = Announcement.query.filter_by(id=id).first()
        if announcement == None:
            return False
        headerID = announcement.headID
        header = User.query.filter_by(id=headerID).first()
        if header.email == username:
            return False
        if isRequestForAnnouncementByUser(id, username):
            return False
        return True

    def getParticipants(id):
        users = getAddedByAnnouncement(id)
        participants = []
        for user in users:
            profile = Profile.query.filter_by(userID=user).first()
            participant = {}
            participant["id"] = user
            participant["name"] = profile.name
            participants.append(participant)
        return participants

    def requestsCount(username):
        userID = User.query.filter_by(email=username).first().id
        announcements = Announcement.query.filter_by(headID=userID).all()
        cnt = 0
        for an in announcements:
            anID = an.id
            requests = Request.query.filter_by(announcementID=anID, status="waiting").all()
            cnt = cnt + len(requests)
        requests = Request.query.filter_by(userID=userID, watchedStatus="notWatched", status="added").all()
        requests = requests + Request.query.filter_by(userID=userID, watchedStatus="notWatched", status="refused").all()
        cnt = cnt + len(requests)
        return cnt
    
    def getRequests(username):
        userID = User.query.filter_by(email=username).first().id
        announcements = Announcement.query.filter_by(headID=userID).all()
        result = []
        for an in announcements:
            anID = an.id
            requests = Request.query.filter_by(announcementID=anID, status="waiting").all()
            for request in requests:
                res = {}
                res["id"] = request.id
                res["type"] = "newRequest"
                res["userName"] = getUserName(request.userID)
                res["userID"] = request.userID
                res["announcementName"] = an.name
                res["announcementID"] = an.id
                res["watchedStatus"] = request.watchedStatus
                result.append(res)
        requests = Request.query.filter_by(userID=userID, status ="added").all()
        requests = requests + Request.query.filter_by(userID=userID, status ="refused").all()
        for request in requests:
            announcement = Announcement.query.filter_by(id=request.announcementID).first()
            res = {}
            res["id"] = request.id
            res["type"] = "notification"
            res["status"] = request.status
            res["watchedStatus"] = request.watchedStatus
            res["announcementID"] = request.announcementID
            res["announcementName"] = announcement.name
            result.append(res)
        return result
    
    def changeWatchedStatus(username):
        userID = User.query.filter_by(email=username).first().id
        requests = Request.query.filter_by(userID=userID).all()
        for request in requests:
            request.watchedStatus = "watched"
        db.session.commit()
        db.session.close()

    def checkIfHeaderByRequest(id, username):
        userID = User.query.filter_by(email=username).first().id
        announcementID = Request.query.filter_by(id=id).first().announcementID
        announcement = Announcement.query.filter_by(id=announcementID).first()
        return announcement.headID == userID
    
    def acceptRequest(id):
        request = Request.query.filter_by(id=id).first()
        request.status = "added"
        makeChat(id)
        db.session.commit()
        db.session.close()
    
    def declineRequest(id):
        request = Request.query.filter_by(id=id).first()
        request.status = "refused"
        db.session.commit()
        db.session.close()

    def getAddedByAnnouncement(id):
        requests = Request.query.filter_by(announcementID = id).all()
        users = []
        for request in requests:
            if request.status == "added":
                users.append(request.userID)
        return users

    def getTravelsByUser(username):
        user = User.query.filter_by(email=username).first()
        requests = Request.query.filter_by(userID=user.id, status="added").all()
        result = []
        for request in requests:
            announcement = Announcement.query.filter_by(id=request.announcementID).first()
            categoryID = announcement.categoryID
            res = (announcement, getCategoryByID(categoryID), getUserEmail(announcement.headID), announcement.headID)
            result.append(res)
        announcements = Announcement.query.filter_by(headID=user.id).all()
        for announcement in announcements:
            categoryID = announcement.categoryID
            res = (announcement, getCategoryByID(categoryID), user.email, user.id)
            result.append(res)
        return result
    
    def getPassedTravelsByUser(userID):
        changeAnnouncementsStatuses()
        user = User.query.filter_by(id = userID).first()
        requests = Request.query.filter_by(userID=userID, status="added").all()
        result = []
        for request in requests:
            announcement = Announcement.query.filter_by(id=request.announcementID).first()
            if announcement.status != "passed":
                continue
            categoryID = announcement.categoryID
            res = (announcement, getCategoryByID(categoryID), getUserEmail(announcement.headID), announcement.headID)
            result.append(res)
        announcements = Announcement.query.filter_by(headID=userID).all()
        for announcement in announcements:
            categoryID = announcement.categoryID
            res = (announcement, getCategoryByID(categoryID), user.email, user.id)
            result.append(res)
        return result
    
    def isRequestForAnnouncementByUser(announcementID, username):
        user = User.query.filter_by(email=username).first()
        request = Request.query.filter_by(userID=user.id, announcementID=announcementID).all()
        if request == []:
            return False
        return True
    
    def checkIfRequestNotRefused(userID, announcementID):
        request = Request.query.filter_by(userID=userID, announcementID=announcementID).all()
        if len(request) == 0:
            return False
        request = request[0]
        if request.status == "refused":
            return False
        return True
    
    def removeParticipant(userID, announcementID):
        request = Request.query.filter_by(userID=userID, announcementID=announcementID).first()
        if request is None:
            pass
        request.status = "deleted"
        db.session.commit()
        db.session.close()