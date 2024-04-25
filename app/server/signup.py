from app import db
from models import User, Profile
from app import app
from flask import session
from app.server.cathegories import getCategoryBikeID, getCategoryMixedID, getCategoryMountsID, getCategorySkisID, getCategoryTrackingID, getCategoryWaterID, addProfileCategory

with app.app_context():
    def register(email, password):
        print(email, password)
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        db.session.close()

    def isRegistered(email):
        user = User.query.filter_by(email = email).first()
        # print(user)
        if user == None:
            return False
        return True

    def userExists(username):
        user = User.query.filter_by(email = username).first()
        print(username, user)
        if user == None:
            return False
        return True
        
    def checkSignin(email, password):
        user = User.query.filter_by(email = email).first()
        if user == None:
            return False
        if user.password == password:
            return True
        return False
    
    def createProfile(username, name, dateOfBirth, gender, info, categoriesTracking, categoriesWater, categoriesSkis, categoriesMounts, categoriesBike, categoriesMixed):
        print("create")
        print(username)
        user = User.query.filter_by(email=username).first()
        userID = user.id
        profile = Profile(userID=userID, email=username, name=name, dateOfBirth=dateOfBirth, gender=gender, info=info)
        db.session.add(profile)
        db.session.commit()
        db.session.close()

        print("profile created")
        print(userID)

        if (categoriesTracking != 'отсутствует'):
            addProfileCategory(userID, getCategoryTrackingID(int(categoriesTracking)))
        if (categoriesWater != 'отсутствует'):
            addProfileCategory(userID, getCategoryWaterID(int(categoriesWater)))
        if (categoriesMounts != 'отсутствует'):
            addProfileCategory(userID, getCategoryMountsID(int(categoriesMounts)))
        if (categoriesSkis != 'отсутствует'):
            addProfileCategory(userID, getCategorySkisID(int(categoriesSkis)))
        if (categoriesBike != 'отсутствует'):
            addProfileCategory(userID, getCategoryBikeID(int(categoriesBike)))
        if (categoriesMixed != 'отсутствует'):
            addProfileCategory(userID, getCategoryMixedID(int(categoriesMixed)))

        print("added")

    def logout():
        session.clear()

    def delete(user):
        thisUser = User.query.filter_by(email = user).first()
        if thisUser:
            db.session.delete(thisUser)
            db.session.commit()

