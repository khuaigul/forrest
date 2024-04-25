from app import db
from app import app
from models import Profile, UserSkill, Category, User, Image
from app.server.cathegories import getCategoriesDictbyUser, updateTracking, updateWater, updateSkis, updateMounts, updateBike, updateMixed


with app.app_context():
    def getProfileData(username):
        data = getCategoriesDictbyUser(username)
        profile = Profile.query.filter_by(email=username).first()

        data["name"] = profile.name
        data["gender"] = profile.gender
        data["dateOfBirth"] = profile.dateOfBirth
        data["info"] = profile.info

        data["Tracking"] = int(data["Tracking"])
        data["Water"] = int(data["Water"])
        data["Skis"] = int(data["Skis"])
        data["Mounts"] = int(data["Mounts"])
        data["Bike"] = int(data["Bike"])
        data["Mixed"] = int(data["Mixed"])


        return data
    
    def getUserIDByUsername(username):
        return User.query.filter_by(email=username).first().id
    
    def getUserEmail(id):
        return User.query.filter_by(id=id).first().email

    def updateProfile(username, name, dateOfBirth, gender, info, Tracking, Water, Skis, Mounts, Bike, Mixed):
        user = User.query.filter_by(email=username).first()
        userID = user.id
        profile = Profile.query.filter_by(userID=userID).first()
        profile.name = name
        profile.dateOfBirth = dateOfBirth
        profile.gender = gender
        profile.info = info
        db.session.commit()
        db.session.close()

        print("UPDATE")

        updateTracking(userID, Tracking)
        updateWater(userID, Water)
        updateSkis(userID, Skis)
        updateMounts(userID, Mounts)
        updateBike(userID, Bike)
        updateMixed(userID, Mixed)

    def getUserName(userID):
        profile = Profile.query.filter_by(userID=userID).first()
        return profile.name
    
    def getUserUsername(userID):
        user = User.query.filter_by(id=userID).first()
        return user.email
    
    def getUserData(id):
        user = User.query.filter_by(id = id).first()
        profile = Profile.query.filter_by(userID=user.id).first()
        data = {}
        data["name"] = profile.name
        data["dateOfBirth"] = profile.dateOfBirth
        categories = getCategoriesDictbyUser(user.email)
        print(categories)
        categoriesList = []
        if categories["Tracking"] != 0:
            categoriesList.append('Пешеходный поход ' + str(categories["Tracking"]))
        if categories["Water"] != 0:
            categoriesList.append('Водный поход ' + str(categories["Water"]))
        if categories["Mounts"] != 0:
            categoriesList.append('Горный поход ' + str(categories["Mounts"]))
        if categories["Skis"] != 0:
            categoriesList.append('Лыжный поход ' + str(categories["Skis"]))
        if categories["Bike"] != 0:
            categoriesList.append('Велосипедный поход ' + str(categories["Bike"]))
        if categories["Mixed"] != 0:
            categoriesList.append('Смешанный поход ' + str(categories["Mixed"]))
        data["categories"] = categoriesList
        return data
    
    def getProfileDocs(username):
        print("USERNAME", username)
        user = User.query.filter_by(email=username).first()
        print(user.id)
        images = Image.query.filter_by(userID=user.id).all()
        return images