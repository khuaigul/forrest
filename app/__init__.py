from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# from flask_uploads import UploadSet, IMAGES, configure_uploads
import os


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

with app.app_context():
   db = SQLAlchemy(app)
   migrate = Migrate(app, db)



# db = SQLAlchemy()
# migrate = Migrate()

# def create_app(config_class=Config):
#    app = Flask(__name__)
#    app.config.from_object(config_class)
#    Bootstrap(app)

#    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
#    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
#    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

#    app.register_blueprint(main_bp)

#    return app

from app import routes

