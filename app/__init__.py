from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# from flask_uploads import UploadSet, IMAGES, configure_uploads
import os


app = Flask(__name__)
app.config.from_object(Config)
# app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
Bootstrap(app)
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
# images = UploadSet('images', IMAGES)
# configure_uploads(app, images)

with app.app_context():
   db = SQLAlchemy(app)
   migrate = Migrate(app, db)



from app import routes