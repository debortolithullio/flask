from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import UploadForm, DatesForm, UploadFormInvestments
from datetime import datetime, date
from app.models import Item
import pandas as pd
from app.utils import *
from app import db

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
   return render_template('index.html', active_page = 'index')

@app.route('/investments', methods=['GET', 'POST'])
def investments():
   form = UploadFormInvestments()
   if form.submit1.data and form.validate():
      flash('Your file was uploaded!')
      return redirect(url_for('investments'))

   #Using session to store the dates used from the last 
   if "init_date_inv" not in session:
      session["init_date_inv"] = date.today().replace(day=1, month=1).strftime("%d%m%Y")
      session["end_date_inv"] = date.today().strftime("%d%m%Y")

   form_date = DatesForm(session["init_date_inv"], session["end_date_inv"])
   if form_date.submit2.data and form_date.validate():
      form_date.initial_date.data = form_date.initial_date.data
      form_date.end_date.data = form_date.end_date.data
      session["init_date_inv"] = form_date.initial_date.data.strftime("%d%m%Y")
      session["end_date_inv"] = form_date.end_date.data.strftime("%d%m%Y")
   elif request.method == 'GET':
      form_date.initial_date.data = datetime.strptime(session["init_date_inv"], "%d%m%Y").date()
      form_date.end_date.data = datetime.strptime(session["end_date_inv"], "%d%m%Y").date()

   return render_template('investments.html', form=form, form_date=form_date, active_page = 'investments')

@app.route('/earnings_and_expenses', methods=['GET', 'POST'])
def earnings_and_expenses():
   form = UploadForm()
   form.origin.choices = [('Credit Card', 'Credit Card'), ('Checking Account', 'Checking Account')]
   if form.submit1.data and form.validate():
      df = pd.read_csv(request.files.get('file_upload'))
      items = create_items(df, form.origin.data)

      for item in items:
         db.session.add(item)
         db.session.commit()

      flash('{} items registered!'.format(len(items)))
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

   #items = Item.query.filter((Item.date >= datetime.strptime(session["init_date_ee"], "%d%m%Y")) & (Item.date <= datetime.strptime(session["end_date_ee"], "%d%m%Y"))).all()
   items_df = pd.read_sql(Item.query.filter((Item.date >= datetime.strptime(session["init_date_ee"], "%d%m%Y")) & (Item.date <= datetime.strptime(session["end_date_ee"], "%d%m%Y"))).statement, db.session.bind) 

   views = get_views_earnings_and_expenses(items_df)

   return render_template('earnings_and_expenses.html', 
                           form=form, 
                           form_date=form_date, 
                           active_page = 'earnings_and_expenses', 
                           views = views)