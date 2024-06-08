from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


setup = False
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
    # if the scheduler has no jobs use the data basde info to load all the jobs
    if len(scheduler.get_jobs()) == 0:
        from.views import myfunc
        with app.app_context():
            schedules = Schedule.query.all()
        for i in schedules:
            trigger = CronTrigger(year="*", month="*", day="*", hour=str(i.timeh), minute=str(i.timem), second="0" )
            scheduler.add_job(myfunc,trigger=trigger,args=["hello world"],id=i.name,replace_existing=True)
        #     print(i)
        #     print(i.timeh, i.timem)
        # print(scheduler.get_jobs())
        # print(len(scheduler.get_jobs()))
    # return app to be used by the rest of the files

    return app

def create_database(app):
    
    if not path.exists("instance\database.db"):
        with app.app_context():
            db.create_all()
        print('Created Database!')