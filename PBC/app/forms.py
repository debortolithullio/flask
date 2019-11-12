from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FileField, SubmitField, validators, RadioField, SelectField, FloatField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired
from wtforms_components import DateRange
from datetime import datetime, date

class UploadForm(FlaskForm):
   origin = RadioField('Origin', validators=[DataRequired()])
   file_upload = FileField("File", validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only!')])
   submit1 = SubmitField("Submit")

class UploadFormInvestments(FlaskForm):
   investment = SelectField("Investment", validators=[DataRequired()], coerce=int)
   date = DateField('Position date', validators=[DataRequired()])
   gross_amount = FloatField('Gross amount', validators=[DataRequired()])
   net_amount = FloatField('Net amount', validators=[DataRequired()])
   submit1 = SubmitField("Insert")

class NewInvestmentForm(FlaskForm):
   category = SelectField("Category", 
                           choices = [('Renda Fixa', 'Renda Fixa'), ('FII', 'FII'), ('Fundos', 'Fundos')], 
                           validators=[DataRequired()])
   title = StringField('Title', validators=[DataRequired()])
   submit3 = SubmitField("Create")

class DatesForm(FlaskForm):
   initial_date = DateField('Initial date', id='datepickinit', validators=[DataRequired()])
   end_date = DateField('End date', id='datepickend', validators=[DataRequired()])
   submit2 = SubmitField("Update views")

   def __init__(self, original_initial_date, original_end_date, *args, **kwargs):
      super(DatesForm, self).__init__(*args, **kwargs)
      self.original_end_date = original_end_date
      self.original_initial_date = original_initial_date

   def validate(self):
      super().validate()
      if self.end_date.data <= self.initial_date.data:
         self.end_date.errors.append('Please the end date has to be greater than initial date.')
         return False
      return True