from app import db
from models import User
from app import app

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
        
    def checkSignin(email, password):
        user = User.query.filter_by(email = email).first()
        if user == None:
            return False
        if user.password == password:
            return True
        return False