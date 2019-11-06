from app.models import Item
import pandas as pd
from datetime import datetime, date

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
   df['grp_date'] = df['date'].apply(lambda x: x.strftime('%B-%Y'))

   if df['grp_date'].nunique() <= 2:
      df['grp_date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))

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