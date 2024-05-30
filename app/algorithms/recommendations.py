from app import app
from models import Request, Announcement, Profile, User
from app.server.requests import getTravelsByUser
from app.server.announcements import getRandomAnnouncements
from app.server.search import stringToList, searchWord

with app.app_context():

    def findKeyWords(str):
        keyWords = set()
        words = set(stringToList(str))
        for word in words:
            if len(word) == 0:
                continue
            if word[0].isupper():
                keyWords.append(word)
        return keyWords


    def getUserRecommendationAlgorithm(userID):
        user = User.query.filter_by(id = userID).first()
        travels = getTravelsByUser(user.email)

        if travels == []:
            return getRandomAnnouncements()

        keyWords = set()
        for announcement, category, headUsername, headID in travels:
            keyWords.union(findKeyWords(announcement.info))
            keyWords.union(findKeyWords(announcement.name))

        records = []
        
        announcements = Announcement.query.filter_by(status="active").all()
        for announcement in announcements:
            name = stringToList(announcement.name)
            info = stringToList(announcement.info)
            words = set(name + info)
            for keyWord in keyWords:
                for word in words:
                    if searchWord(word, keyWord):
                        records.append(announcement)

        if len(records) < 10:
            records = records + getRandomAnnouncements(10 - len(records))
        
        return records

