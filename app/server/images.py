from app import app
from flask import send_from_directory, url_for
from app import ALLOWED_EXTENSIONS
from flask_uploads import configure_uploads, IMAGES, UploadSet
from app.server.profile import getUserIDByUsername
from models import Image
from app import db
import pathlib

with app.app_context():

    def get_file(filename):
        return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

    def allowed_file(file):
        return pathlib.Path(file.filename).suffix in ALLOWED_EXTENSIONS
    
    def getDocNameForUser(username):
        userID = getUserIDByUsername(username)
        docs = Image.query.filter_by(userID=userID).all()
        filename = str(userID) + "document" + str(len(docs))
        return filename
    
    def createDocument(username, filename, name,):
        userID = getUserIDByUsername(username)
        doc = Image(userID=userID, filename=filename, name=name)
        db.session.add(doc)
        db.session.commit()
        db.session.close()

        