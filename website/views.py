from flask import Blueprint,url_for,render_template,request,redirect,flash
from flask_login import login_required, current_user
import time
from . import db
from .models import Schedule
from datetime import datetime
 
def convert24(time):
    # Parse the time string into a datetime object
    t = datetime.strptime(time, '%I %p')
    # Format the datetime object into a 24-hour time string
    return t.strftime('%H')
 
def time_format(hrs,min,per):
    hrs = str(hrs)
    t = datetime.strptime(str(min), '%M')
    min = t.strftime('%M')
    final = hrs+":"+min+" "+per
    return final
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
    return render_template("schedule.html", user=current_user,no_sched = len(current_user.Schedule) ,schedules = Schedule.query.all()
)

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

                    new_schedule = Schedule( name = name_of_schedule ,timeh = int(convert24(str(TODh)+" "+ per_of_day)) , timem = TODm,time12=time_format(TODh,TODm,per_of_day), per_of_day = per_of_day , duration = duration , user_id = current_user.id)
                    db.session.add(new_schedule)
                    db.session.commit()
                    schedules = Schedule.query.all()
                    for i in schedules:
                        print(i.name)
                    flash("Added succesfully" , "succes")
                    return redirect(url_for('views.schedule'))
            else:

                flash("You have to input a value for duration." ,category='error')
        else:
            flash("You have to input a value for time." ,category="error")
    return render_template("add_sched.html", user=current_user)