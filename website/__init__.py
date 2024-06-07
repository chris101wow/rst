from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Just giving the database a name and a location 
db = SQLAlchemy()
DB_NAME = "database.db"
scheduler = BackgroundScheduler()
scheduler.start() 
def create_app():
    # Initialize flask 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chris is cool'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # Make routes known to app
    from .views import views
    from .auth import auth
    # Define url prefix where to go to get certain pages and routes
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    # Create the database 
    from .models import User, Schedule

    create_database(app)
    # Initialize login manager 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # return app to be used by the rest of the files
    return app


def create_database(app):
    
    if not path.exists("instance\database.db"):
        with app.app_context():
            db.create_all()
        print('Created Database!')