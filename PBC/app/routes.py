from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import UploadForm, DatesForm
from datetime import datetime, date

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
   return render_template('index.html', active_page = 'index')

@app.route('/investments', methods=['GET', 'POST'])
def investments():
   form = UploadForm()
   if form.validate_on_submit():
      flash('Your file was uploaded!')
      return redirect(url_for('investments'))
   return render_template('investments.html', active_page = 'investments')

@app.route('/earnings_and_expenses', methods=['GET', 'POST'])
def earnings_and_expenses():
   form = UploadForm()
   if form.submit1.data and form.validate():
      flash('Your file was uploaded!')
      return redirect(url_for('earnings_and_expenses'))

   #Using session to store the dates used from the last 
   if "init_date_ee" not in session:
      session["init_date_ee"] = date.today().replace(day=1, month=1).strftime("%d%m%Y")
      session["end_date_ee"] = date.today().strftime("%d%m%Y")

   form_date = DatesForm(session["init_date_ee"], session["end_date_ee"])
   if form_date.submit2.data and form_date.validate():
      form_date.initial_date.data = form_date.initial_date.data
      form_date.end_date.data = form_date.end_date.data
      session["init_date_ee"] = form_date.initial_date.data.strftime("%d%m%Y")
      session["end_date_ee"] = form_date.end_date.data.strftime("%d%m%Y")
   elif request.method == 'GET':
      form_date.initial_date.data = datetime.strptime(session["init_date_ee"], "%d%m%Y").date()
      form_date.end_date.data = datetime.strptime(session["end_date_ee"], "%d%m%Y").date()

   return render_template('earnings_and_expenses.html', form=form, form_date=form_date, active_page = 'earnings_and_expenses')