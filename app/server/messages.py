from models import User, Message, Chat, Request, Announcement, Profile
from datetime import datetime
from app import db
from app.server.profile import getUserUsername, getUserName
from app import app
from operator import itemgetter, attrgetter

with app.app_context():

    def createChat(firstUserID, secondUserID):
        chat = Chat(firstUserID=firstUserID, secondUserID=secondUserID, status="open")
        db.session.add(chat)
        db.session.commit()
        db.session.close()
    
    def getChatID(user1ID, user2ID):
        chat = Chat.query.filter_by(firstUserID=user1ID, secondUserID=user2ID).all()
        if chat == []:
            chat = Chat.query.filter_by(firstUserID=user2ID, secondUserID=user1ID).all()
        if chat == []:
            return
        chat = chat.first()
    
    def makeChat(requestID):
        request = Request.query.filter_by(id=requestID).first()
        firstUserID = request.userID
        announcement = Announcement.query.filter_by(id=request.announcementID).first()
        secondUserID = announcement.headID
        createChat(firstUserID, secondUserID)
    
    def getChatUnreadedCount(chatID, userID, memberID):
        messages = Message.query.filter_by(chatID=chatID,firstUserID=memberID, status="notWatched").all()
        return len(messages)

    def getChats(username):
        user = User.query.filter_by(email=username).first()
        chats = Chat.query.filter_by(firstUserID=user.id).all()
        chats = chats + Chat.query.filter_by(secondUserID=user.id).all()
        result = []
        for chat in chats:
            res = {}
            res["id"] = chat.id
            memberID = User.query.filter_by(id=chat.firstUserID).first().id
            if user.id == chat.firstUserID:
                memberID = User.query.filter_by(id=chat.secondUserID).first().id
            memberProfile = Profile.query.filter_by(userID=memberID).first()
            res["name"] = memberProfile.name
            res["count"] = getChatUnreadedCount(chat.id, user.id, memberID)
            result.append(res)
        return result
    
    def getMessagesByChatID(chatID):
        messages = Message.query.filter_by(chatID=chatID).all()
        return messages
    
    def getMessages(chatID):
        records = []
        messages = getMessagesByChatID(chatID)
        for message in messages:
            record = {}
            record["text"] = message.text
            record["firstUserName"] = getUserUsername(message.firstUserID)
            record["secondUserName"] = getUserUsername(message.secondUserID)
            record["status"] = message.status
            record["dateTime"] = message.sendTime
            record["firstName"] = getUserName(message.firstUserID)
            record["secondName"] = getUserName(message.secondUserID)
            records.append(record)
        sorted(records, key=lambda x: x['dateTime'])
        records.reverse()
        return records

    def sendMessage(username, text, chatID):
        user = User.query.filter_by(email=username).first()
        chat = Chat.query.filter_by(id=chatID).first()
        memberID = User.query.filter_by(id=chat.firstUserID).first().id
        if user.id == chat.firstUserID:
            memberID = User.query.filter_by(id=chat.secondUserID).first().id
        message = Message(text=text, firstUserID=user.id, chatID=chatID, secondUserID=memberID, status="notWatched", sendTime=datetime.now())
        db.session.add(message)
        db.session.commit()
        db.session.close()

    def makeWathed(chatID, username):
        user = User.query.filter_by(email=username).first()
        messages = Message.query.filter_by(chatID=chatID, secondUserID=user.id).all()
        for message in messages:
            message.status = "watched"
        db.session.commit()
        db.session.close()

    def getLastMessage(chatID):
        messages = Message.query.filter_by(chatID=chatID).all()
        sorted(messages, key=Message.sendTime)
        if messages == []:
            return None
        return messages[0].text

    def checkIfChatAllowed(chatID, username):
        user = User.query.filter_by(email=username).first()
        chat = Chat.query.filter_by(id=chatID).first()
        if chat == None:
            return False
        return (user.id == chat.firstUserID or user.id == chat.secondUserID)