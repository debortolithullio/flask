from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import UploadForm, DatesForm, UploadFormInvestments, NewInvestmentForm
from datetime import datetime, date
from app.models import Item, Investment, Position
import pandas as pd
from app.utils import *
from app import db

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
   return render_template('index.html', active_page = 'index')

@app.route('/investments', methods=['GET', 'POST'])
def investments():
   new_inv_form = NewInvestmentForm()
   if new_inv_form.submit3.data and new_inv_form.validate():
      new_investment = Investment(title=new_inv_form.title.data, category=new_inv_form.category.data)
      db.session.add(new_investment)
      db.session.commit()

      flash('New investment created!')
      return redirect(url_for('investments'))

   form = UploadFormInvestments()
   investments = Investment.query.all()
   form.investment.choices = [(inv.id, inv.title) for inv in investments]
   if form.submit1.data and form.validate():
      new_position = Position(investment=form.investment.data, date=form.date.data, net_amount=form.net_amount.data, gross_amount=form.gross_amount.data)
      db.session.add(new_position)
      db.session.commit()

      flash('New position inserted!')
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

   positions_df = pd.read_sql(Position.query.filter((Position.date >= datetime.strptime(session["init_date_inv"], "%d%m%Y")) & (Position.date <= datetime.strptime(session["end_date_inv"], "%d%m%Y"))).statement, db.session.bind) 
   investments_df = pd.read_sql(Investment.query.statement, db.session.bind) 
   investments_df = pd.merge(positions_df, investments_df, how = 'left', left_on = 'investment', right_on = 'id')
   views = get_views_investment(investments_df)

   return render_template('investments.html', 
                           new_inv_form=new_inv_form, 
                           form=form, 
                           form_date=form_date, 
                           active_page = 'investments',
                           views = views)

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