from flask import Flask
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class QuestionForm(FlaskForm):
    question = StringField('Question', validators = [DataRequired()])
    option1 = StringField('Option1', validators = [DataRequired()])
    option2 = StringField('Option2', validators = [DataRequired()])
    submit = SubmitField("Ask !!")