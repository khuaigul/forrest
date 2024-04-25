from models import Category, Profile, UserSkill
from app import db
from app import app

with app.app_context():
    def create_caths():
        typesList = ['Tracking', 'Water', 'Skis', 'Mounts', 'Bike', 'Mixed']
        for el in typesList:
            newCath = Category(sportStatus="non-sport", sportType=el, category=None)
            db.session.add(newCath)
            newpwd = Category(sportStatus="weekend", sportType=el, category=None)
            db.session.add(newpwd)
            for i in range(1, 7):
                newCath = Category(sportStatus="sport", sportType=el, category=i)
                db.session.add(newCath)
            
        db.session.commit()
        db.session.close()
    
    def getNameDict():
        dict = {}
        dict['Tracking'] = 'Пешеходный'
        dict['Water'] = 'Водный'
        dict['Mounts'] = 'Горный'
        dict['Skis'] = 'Лыжный'
        dict['Mixed'] = 'Смешанный'
        dict['Bike'] = 'Велосипедный'

        return dict
    
    def getCategoryByID(categoryID):
        print("get Category by ID ", categoryID)
        cat = Category.query.filter_by(id=categoryID).first()
        nameDict = getNameDict()
        name = ""
        if cat.sportStatus == "non-sport":
            name = "неспортивный "
        
        name += nameDict[cat.sportType] + " "

        if cat.sportStatus == "weekend":
            name += "поход выходного дня "
        if cat.sportStatus == "sport":
            name += str(cat.category)

        return name
    
    def getCategoryIDByType(sportStatus, sportType, category = None):
        # print(sportStatus, sportType, category)
        category = Category.query.filter_by(sportStatus=sportStatus, sportType=sportType, category=category).first()
        if category == None:
            return None
        return category.id
    

    def getAllCategories():
        categories = Category.query.all()
        categoryList = []
        for cat in categories:
            catID = cat.id
            
            name = getCategoryByID(catID)

            categoryList.append((catID, name))

        return categoryList


    def getTypeList():
        return ['Tracking', 'Water', 'Skis', 'Mounts', 'Bike', 'Mixed']

    first_record = Category.query.all()
    if first_record == None:
        create_caths()

    def getCategories():
        first_record = Category.query.all()
        if not first_record:
            create_caths()
        return Category.query.filter_by(sportStatus = "sport").all()
    
    def categoryCountList():
        lst = []
        for i in range(0, 7):
            lst.append(str(i))
        return lst

    def getCategoryTrackingID(val):
        val = int(val)
        print("get categori tracking id")
        categories = Category.query.filter_by().all()
        if categories == []:
            create_caths()
        if val == 0:
            return -1
        sportType = "Tracking"
        categories = Category.query.filter_by(sportStatus="sport", category=val, sportType=sportType).first()
        print("catt")
        print(categories.id)
        return categories.id
    
    def getCategoryWaterID(val):
        val = int(val)
        categories = Category.query.filter_by().all()
        if categories == []:
            create_caths()
        if val == 0:
            return -1
        sportType = "Water"
        print("val is 0")
        print(type(val), type(0))
        print(val == 0, val, 0)
        categories = Category.query.filter_by(sportStatus="sport", category=val, sportType=sportType).first()
        return categories.id
    
    def getCategoryMountsID(val):
        val = int(val)

        categories = Category.query.filter_by().all()
        if categories == []:
            create_caths()
        if val == 0:
            return -1
        sportType = "Mounts"
        categories = Category.query.filter_by(sportStatus="sport", category=val, sportType=sportType).first()
        return categories.id
    
    def getCategorySkisID(val):
        val = int(val)

        categories = Category.query.filter_by().all()
        if categories == []:
            create_caths()
        if val == 0:
            return -1
        sportType = "Skis"
        categories = Category.query.filter_by(sportStatus="sport", category=val, sportType=sportType).first()
        return categories.id
    
    def getCategoryBikeID(val):
        val = int(val)

        categories = Category.query.filter_by().all()
        if categories == []:
            create_caths()
        if val == 0:
            return -1
        sportType = "Bike"
        categories = Category.query.filter_by(sportStatus="sport", category=val, sportType=sportType).first()
        return categories.id
    
    def getCategoryMixedID(val):
        val = int(val)

        categories = Category.query.filter_by().all()
        if categories == []:
            create_caths()
        if val == 0:
            return -1
        sportType = "Mixed"
        categories = Category.query.filter_by(sportStatus="sport", category=val, sportType=sportType).first()
        return categories.id
    
    def addProfileCategory(userID, categoryID):
        print("add profile category", categoryID)
        if categoryID == -1:
            return
        userSkill = UserSkill(userID=userID, categoryID=categoryID)
        db.session.add(userSkill)
        db.session.commit()
        db.session.close()

    def getCategoriesDictbyUser(username):
        profile = Profile.query.filter_by(email=username).first()
        userID = profile.userID
        skills = UserSkill.query.filter_by(userID=userID).all()
        categories = {}

        for skill in skills:
            categoryID = skill.categoryID
            category = Category.query.filter_by(id = categoryID).first()
            if category.sportStatus == "sport":
                categories[category.sportType] = (category.category)
            categories[category.sportType] = str(categories[category.sportType])        

        typeList = getTypeList()
        for type in typeList:
            if type not in categories:
                categories[type] = 0


        return categories
    
    def updateTracking(userID, value):
        userSkills = UserSkill.query.filter_by(userID=userID).all()
        flag = False
        for skill in userSkills:
            if isType(skill.categoryID, "Tracking"):
                flag = True
                if value == '0':
                    db.session.delete(skill)
                    db.session.commit()
                else:
                    skill.categoryID = getCategoryTrackingID(value)
                    db.session.commit()
        if not flag:
            categoryID = getCategoryTrackingID(value)
            addProfileCategory(userID, categoryID)
        
    def updateWater(userID, value):
        userSkills = UserSkill.query.filter_by(userID=userID).all()
        flag = False
        for skill in userSkills:
            if isType(skill.categoryID, "Water"):
                flag = True
                if value == '0':
                    db.session.delete(skill)
                    db.session.commit()
                else:
                    skill.categoryID = getCategoryWaterID(value)
                    db.session.commit()
        if not flag:
            categoryID = getCategoryWaterID(value)
            addProfileCategory(userID, categoryID)

    def updateSkis(userID, value):
        userSkills = UserSkill.query.filter_by(userID=userID).all()
        flag = False
        for skill in userSkills:
            if isType(skill.categoryID, "Skis"):
                flag = True
                if value == '0':
                    db.session.delete(skill)
                    db.session.commit()
                else:
                    skill.categoryID = getCategorySkisID(value)
                    db.session.commit()
        if not flag:
            categoryID = getCategorySkisID(value)
            addProfileCategory(userID, categoryID)

    def updateMounts(userID, value):
        print("UPDATE MOUNTS", value)
        userSkills = UserSkill.query.filter_by(userID=userID).all()
        flag = False
        print("UPDATE VALUE", value)
        for skill in userSkills:
            if isType(skill.categoryID, "Mounts"):
                flag = True
                if value == '0':
                    db.session.delete(skill)
                    db.session.commit()
                else:
                    skill.categoryID = getCategoryMountsID(value)
                    db.session.commit()
        if not flag:
            categoryID = getCategoryMountsID(value)
            addProfileCategory(userID, categoryID)

    def updateBike(userID, value):
        userSkills = UserSkill.query.filter_by(userID=userID).all()
        flag = False
        for skill in userSkills:
            if isType(skill.categoryID, "Bike"):
                flag = True
                if value == '0':
                    db.session.delete(skill)
                    db.session.commit()
                else:
                    skill.categoryID = getCategoryBikeID(value)
                    db.session.commit()
        if not flag:
            categoryID = getCategoryBikeID(value)
            addProfileCategory(userID, categoryID)


    def updateMixed(userID, value):
        userSkills = UserSkill.query.filter_by(userID=userID).all()
        flag = False
        for skill in userSkills:
            if isType(skill.categoryID, "Mixed"):
                flag = True
                if value == '0':
                    db.session.delete(skill)
                    db.session.commit()
                else:
                    skill.categoryID = getCategoryMixedID(value)
                    db.session.commit()
        if not flag:
            categoryID = getCategoryMixedID(value)
            addProfileCategory(userID, categoryID)


    def isType(categoryID, type):
        category = Category.query.filter_by(id=categoryID).first()
        categoryType = category.sportType
        return categoryType == type
