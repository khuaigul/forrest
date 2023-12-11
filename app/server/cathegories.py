from models import Category
from app import db
from app import app

with app.app_context():
    def create_caths():
        # first_record = Category.query.first()
        # if first_record == None:
        typesList = ['Пешеходный', 'Водный', 'Лыжный', 'Горный', 'Велосипедный', 'Смешанный']
        for el in typesList:
            newCath = Category(sportStatus="non-sport", sportType=el, category=None)
            db.session.add(newCath)
            newpwd = Category(sportStatus="weekend", sportType=el, category=None)
            db.session.add(newpwd)
            for i in range(1, 6):
                newCath = Category(sportStatus="sport", sportType=el, category=i)
                db.session.add(newCath)
            
        db.session.commit()
        db.session.close()

    first_record = Category.query.all()
    if first_record == None:
        create_caths()

    sportTypes = ['Пешеходный', 'Водный', 'Лыжный', 'Горный', 'Велосипедный', 'Смешанный']
    sportCategories = [i for i in range(1, 6)]
    
