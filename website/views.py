from flask import Blueprint,url_for,render_template,request,redirect,flash
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
        print(request.form )
        name_of_schedule = request.form.get("sched_name")
        TODh = request.form.get("TODh")
        TODm = request.form.get("TODm")
        per_of_day = request.form.get("per_of_day")
        duration = request.form.get("dura")
        if len(TODh) > 0 and len(TODm) > 0:
            TODh = int(TODh)
            TODm = int(TODm)
            if len(duration) > 0:
                duration = int(duration)
                if len(name_of_schedule) == 0:
                    flash("Must enter a name for the schedule" ,category='error')
                elif TODh > 12  or TODh < 1:
                    flash("Invalid input for hourly time." ,category='error') 
                elif TODm > 59  or TODm < 0:
                    flash("Invalid input for time in minutes." ,category='error')
                elif duration < 0:
                    flash("Duration must be greater than 0 seconds." ,category='error')
                else:
                    return redirect(url_for('views.home'))
            else:
                flash("You have to input a value for duration." ,category='error')
        else:
            flash("You have to input a value for time." ,category="error")
    return render_template("add_sched.html", user=current_user)