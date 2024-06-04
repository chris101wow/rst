from flask import Blueprint,url_for,render_template,request,redirect
from flask_login import login_required, current_user
import time
from .models import Schedule

# Local time has date and time


views = Blueprint('views',__name__)
#create route (base route)
def tod():
    t = time.localtime()
    if t.tm_hour>=12:
        return "Evening "
    return "Morning "

@views.route('/',methods=["GET","POST"])
@login_required
def home():
    print()
    return render_template("home.html", user=current_user,greet_per = tod())
@views.route("/schedules")
@login_required
def schedule():
    return render_template("schedule.html", user=current_user,no_sched = len(current_user.Schedule))

@views.route('/add_sched', methods=["GET","POST"])
@login_required
def add_sched():
    if request.method == "POST":
         print(request.form)
         return redirect(url_for('views.home'))
    return render_template("add_sched.html", user=current_user)