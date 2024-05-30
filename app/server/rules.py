from app import app
from app.server.profile import getUserIDByUsername
from app.server.announcements import checkIfHeader, userGoesWithUser, userHaveAnnouncements
from app.server.requests import checkIfRequestNotRefused

with app.app_context():
    
    def checkIfUserAllowed(username, userID):
        ID = getUserIDByUsername(username)
        if userHaveAnnouncements(ID):
            return True
        return userGoesWithUser(ID, userID)
    
    def checkIfParticipantsAllowed(username, announcementID):
        if checkIfHeader(username, announcementID):
            return True
        userID = getUserIDByUsername(username)
        return checkIfRequestNotRefused(userID, announcementID)
    

        