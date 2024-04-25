from app import app
from app.algorithms.recommendations import getUserRecommendationAlgorithm
from app.server.profile import getUserEmail
from app.server.cathegories import getCategoryByID
from app.server.announcements import changeAnnouncementsStatuses
from models import User

with app.app_context():

    def getUserRecommendations(username):
        changeAnnouncementsStatuses()
        user = User.query.filter_by(email=username).first()
        announcements = getUserRecommendationAlgorithm(user.id)

        records = []
        for announcement in announcements:
            print("ANNOUNCEMENT", announcement)
            records.append((announcement, getCategoryByID(announcement.categoryID), getUserEmail(announcement.headID), announcement.headID))
        return records