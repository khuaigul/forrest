from app import app
from app.server.cathegories import getCategoryByID, getCategoryIDByType
from app.server.announcements import getAnnouncementsByFilters, changeAnnouncementsStatuses
from models import User, Announcement
from Levenshtein import ratio

with app.app_context():

    def getSearchResult(searchString, tracking, water, mounts, skis, bike, mixed, pvd, nonsport, category1, category2, category3, category4, category5, category6, dateBegin, dateEnd):
        if searchString == "":
            return []
        categories = []
        if not tracking and not water and not mounts and not skis and not bike and not mixed:
            tracking = water = mounts = skis = bike = mixed = True
        if not pvd and not nonsport and not category1 and not category2  and not category3 and not category4 and not category5 and not category6:
            pvd = nonsport = category1 = category2 = category3 = category4 = category5 = category6 = True
        
        sportCategories = [category1, category2, category3, category4, category5, category6]
        sportTypes = {"Tracking" : tracking, "Water" : water, "Mounts" : mounts, "Skis" : skis, "Bike" : bike, "Mixed" : mixed}
        for sportType, flag in sportTypes.items():
            if not flag:
                continue
            if pvd:
                categories.append(getCategoryIDByType("weekend", sportType))
            if nonsport:
                categories.append(getCategoryIDByType("non-sport", sportType))
            for i in range(6):
                num = i + 1
                if sportCategories[i]:
                    categories.append(getCategoryIDByType("sport", sportType, str(num)))
        categoryAnnouncementsIDS = getAnnouncementsByFilters(categories, dateBegin, dateEnd)
        announcements = searchByText(categoryAnnouncementsIDS, searchString)
        return announcements
    
    def stringToList(text):
        return str(text).lower().replace('.', ' ').replace('\n', ' ').replace('-', ' ').replace(',', ' ').replace('.', ' ').replace("  ", ' ').split(' ')
    
    def searchByText(announcementsIDS, text):
        records = []
        textString = stringToList(text)
        for announcementID in announcementsIDS:
            announcement = Announcement.query.filter_by(id=announcementID).first()
            value = 0
            name = announcement.name
            info = announcement.info
            name = stringToList(name)
            info = stringToList(info)
            for text in textString:
                for word in name:
                    if searchWord(word, text):
                        value = value + 1
                for word in info:
                    if searchWord(word, text):
                        value = value + 1
            record = {}
            if value > 0:
                if not announcement.status == "active":
                    value = 1.0 / value
                record["value"] = value
                record["announcement"] = announcement
                records.append(record)
        records = sorted(records, key=lambda d: d['value'])
        records.reverse()
        announcements = []
        for record in records:
            head = User.query.filter_by(id=record["announcement"].headID).first()
            announcements.append((record["announcement"], getCategoryByID(record["announcement"].categoryID), head.email, head.id))
        return announcements
    
    def searchWord(word, text):
        score = ratio(word, text)
        return score > 0.6
    
    