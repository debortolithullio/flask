from app.models import Item
import pandas as pd
from datetime import datetime, date
from app.models import Item, Investment, Position
from app import db

def create_items(df, origin):
   '''
   Function to clean dataframe and create Items to be inserted in the database
   '''
   if origin == 'Credit Card':
      # Check chargeback
      df_aux = df[df.amount < 0]
      for index_aux, row_aux in df_aux.iterrows():
         for index, row in df.iterrows():
            if -row.amount == row_aux.amount and row.title.lower() in row_aux.title.lower():
               df.drop(index = [index, index_aux], inplace = True)
               break

      df['mtype'] = ['expense' if row.amount > 0 else 'earning' for index, row in df.iterrows()]

   elif origin == "Checking Account":
      df['mtype'] = ['expense' if row.amount < 0 else 'earning' for index, row in df.iterrows()]
   
   df['category'] = df['category'].fillna('others')
   df['amount'] = abs(df.amount)

   return [Item(title = row['title'], 
                  category = row['category'], 
                  date = datetime.strptime(row['date'], "%Y-%m-%d"), 
                  amount = row['amount'],
                  mtype = row['mtype']) for index, row in df.iterrows()]

def get_views_earnings_and_expenses(df):
   df['grp_date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))

   if df['grp_date'].nunique() <= 2:
      df['grp_date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

   group_df = df.groupby(by=['grp_date', 'category', 'mtype']).sum().reset_index()[['grp_date', 'category', 'mtype', 'amount']]
   general_df = df.groupby(by=['grp_date', 'mtype']).sum().reset_index()[['grp_date', 'mtype', 'amount']].sort_values(by=['grp_date'])
   
   merge_general = pd.merge(general_df[general_df.mtype == "earning"], general_df[general_df.mtype == "expense"], how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0).sort_values(by=['grp_date'])

   categories_merge = {}
   for cat in list(group_df['category'].unique()):
      g_ear = pd.merge(pd.DataFrame(group_df['grp_date'].unique(), columns=["grp_date"]), group_df[(group_df.mtype == "earning") & (group_df.category == cat)], how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0)
      g_exp = pd.merge(pd.DataFrame(group_df['grp_date'].unique(), columns=["grp_date"]), group_df[(group_df.mtype == "expense") & (group_df.category == cat)], how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0)
      categories_merge[cat] = pd.merge(g_ear, g_exp, how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0)

   views = {}

   # General Chart
   views['general_labels'] = list(general_df['grp_date'].unique())
   views['general_label1'] = "Earnings"
   views['general_label2'] = "Expenses"
   views['general_data1'] = list(merge_general['amount_x'])
   views['general_data2'] = list(merge_general['amount_y'])

   # Stacked by category chart
   views['stack_labels'] = list(group_df['grp_date'].unique())
   views["stack-earnings"] = {}
   views["stack-expenses"] = {}
   for cat, merge_df in categories_merge.items(): 
      if sum(merge_df['amount_x'])>0:
         views["stack-earnings"][cat] = {}
         views["stack-earnings"][cat]['data1'] = list(merge_df['amount_x'])
      if sum(merge_df['amount_y'])>0:
         views["stack-expenses"][cat] = {}
         views["stack-expenses"][cat]['data2'] = list(merge_df['amount_y'])

   return views 

def get_views_investment(df):
   df['grp_date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
   df.drop_duplicates(subset=['grp_date', 'category', 'title'], keep='last', inplace = True)

   group_df = df.groupby(by=['grp_date', 'category']).sum().reset_index()[['grp_date', 'category', 'net_amount']].sort_values(by=['grp_date'])
   general_df = df.groupby(by=['grp_date', 'title']).sum().reset_index()[['grp_date', 'title', 'net_amount']].sort_values(by=['grp_date'])
   
   views = {}

   views['general_labels'] = list(general_df['grp_date'].unique())
   views['category_labels'] = list(group_df['grp_date'].unique())
   views["general"] = {}
   views["category"] = {}
   for title in list(general_df.title.unique()):
      aux_df = pd.merge(pd.DataFrame(general_df['grp_date'].unique(), columns=["grp_date"]), general_df[general_df.title == title], how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0)
      views["general"][title] = {}
      views["general"][title]['data'] = list(aux_df['net_amount'])

   for category in list(group_df.category.unique()):
      aux_df = pd.merge(pd.DataFrame(group_df['grp_date'].unique(), columns=["grp_date"]), group_df[group_df.category == category], how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0)
      views["category"][category] = {}
      views["category"][category]['data'] = list(aux_df['net_amount'])

   return views 

def get_views_dashboard(year, categories_to_ignore=None):
   init_date = datetime.strptime('0101'+year, "%d%m%Y").date()
   end_date = datetime.strptime('3112'+year, "%d%m%Y").date()

   #get data
   positions_df = pd.read_sql(Position.query.filter((Position.date >= init_date) & (Position.date <= end_date)).statement, db.session.bind) 
   df_investment = pd.read_sql(Investment.query.statement, db.session.bind) 
   df_investment = pd.merge(positions_df, df_investment, how = 'left', left_on = 'investment', right_on = 'id')
   df_earnings_and_expenses = pd.read_sql(Item.query.filter((Item.date >= init_date) & (Item.date <= end_date)).statement, db.session.bind) 

   #group
   df_investment['grp_date'] = df_investment['date'].apply(lambda x: x.strftime('%Y-%m'))
   df_investment.drop_duplicates(subset=['grp_date', 'category', 'title'], keep='last', inplace = True)
   df_investment = df_investment.groupby(by=['grp_date']).sum().reset_index()[['grp_date', 'gross_amount', 'net_amount']].sort_values(by=['grp_date'])

   df_earnings_and_expenses['grp_date'] = df_earnings_and_expenses['date'].apply(lambda x: x.strftime('%Y-%m'))
   if categories_to_ignore:
      df_earnings_and_expenses = df_earnings_and_expenses[~df_earnings_and_expenses.category.isin(categories_to_ignore)]
   df_earnings_and_expenses = df_earnings_and_expenses.groupby(by=['grp_date', 'mtype']).sum().reset_index()[['grp_date', 'mtype', 'amount']].sort_values(by=['grp_date'])
   df_earnings_and_expenses = pd.merge(df_earnings_and_expenses[df_earnings_and_expenses.mtype == "earning"], df_earnings_and_expenses[df_earnings_and_expenses.mtype == "expense"], how = 'outer', left_on = 'grp_date', right_on = 'grp_date').fillna(0).sort_values(by=['grp_date'])


   views = {}
   # Investment informations
   views['year_variation_percentage'] = float("{0:.2f}".format(((df_investment['net_amount'].iloc[-1]/df_investment['net_amount'].iloc[0])-1)*100))
   views['year_total_amount'] = float("{0:.2f}".format(df_investment['net_amount'].iloc[-1]))
   views['inv_chart_labels'] = list(df_investment['grp_date'].unique())
   views['inv_chart_label1'] = "Net amount"
   views['inv_chart_label2'] = "Gross amount"
   views['inv_chart_data1'] = list(df_investment['net_amount'])
   views['inv_chart_data2'] = list(df_investment['gross_amount'])

   # Earnings and expenses informations
   views['year_earnings'] = float("{0:.2f}".format(sum(list(df_earnings_and_expenses['amount_x']))))
   views['year_expenses'] = float("{0:.2f}".format(sum(list(df_earnings_and_expenses['amount_y']))))
   views['ee_chart_labels'] = list(df_earnings_and_expenses['grp_date'].unique())
   views['ee_chart_label1'] = "Earnings"
   views['ee_chart_label2'] = "Expenses"
   views['ee_chart_data1'] = list(df_earnings_and_expenses['amount_x'])
   views['ee_chart_data2'] = list(df_earnings_and_expenses['amount_y'])

   return views
