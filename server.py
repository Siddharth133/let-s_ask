from flask import Flask, render_template, url_for, flash, redirect, request, abort
from dotenv import load_dotenv
import os
from forms import QuestionForm
from models import Question
from datetime import datetime
from sqlalchemy.sql.expression import func
from flask_sqlalchemy import SQLAlchemy

# Initialize the db variable without an app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    
    # Include your models here (Question)
    class Question(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        question = db.Column(db.String(100), nullable=False)
        date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        option1 = db.Column(db.Text, nullable=False)
        option2 = db.Column(db.Text, nullable=False)
        count1 = db.Column(db.Integer, nullable=False, default=0)
        count2 = db.Column(db.Integer, nullable=False, default=0)

        def __repr__(self):
            return f"Question('{self.question}', '{self.date_posted}')"

    # Register your routes
    @app.route("/")
    @app.route("/home")
    def home():
        page = request.args.get('page', 1, type=int)
        trending = Question.query.order_by((Question.count1 + Question.count2).desc()).limit(5).all()
        questions = Question.query.order_by(func.random()).paginate(per_page=10, page=page)
        return render_template("index.html", questions=questions, trending=trending)

    @app.route("/add_ques", methods=['GET', 'POST'])
    def add_ques():
        form = QuestionForm()
        if form.validate_on_submit():
            ques = Question(question=form.question.data, option1=form.option1.data, option2=form.option2.data)
            db.session.add(ques)
            db.session.commit()
            flash("Your question has been added!", 'success')
            return redirect(url_for('home'))
        return render_template("add_question.html", form=form)

    @app.route("/vote/<int:question_id>/<option>")
    def vote(question_id, option):
        question = Question.query.get_or_404(question_id)
        if option == 'option1':
            question.count1 += 1
        elif option == 'option2':
            question.count2 += 1
        else:
            return abort(404)
        db.session.commit()
        flash('Your vote has been recorded.', 'success')
        return redirect(url_for('home'))
    return app
   


# from flask import Flask
# from dotenv import load_dotenv,dotenv_values
# import os
# from flask import render_template, url_for, flash, redirect,request,abort
# from forms import QuestionForm
# from models import Question
# from datetime import datetime
# from sqlalchemy.sql.expression import func
# from extensions import db
# from flask_sqlalchemy import SQLAlchemy
# load_dotenv()
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SECRET_KEY'] = '32811a5e6f0d2b4e26069182db09d329'
# # postgres://question_afyi_user:hqNWu35rSFnrWI0YM0vpGkyYzQEsDJD8@dpg-cniq7po21fec73ctf6jg-a.oregon-postgres.render.com/question_afyi
# db = SQLAlchemy(app)

# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False,
#                             default=datetime.utcnow)
#     option1 = db.Column(db.Text, nullable=False)
#     option2 = db.Column(db.Text, nullable=False)
#     count1 = db.Column(db.Integer, nullable=False,default = 0)
#     count2 = db.Column(db.Integer, nullable=False,default = 0)
    

#     def __repr__(self):
#         return f"Post('{self.question}','{self.date_posted}')"

# @app.route("/")
# @app.route("/home")
# def home():
#     page = request.args.get('page', 1, type=int)
#     # Query for getting top 5 trending question based on total count
#     trending = db.session.query(Question).order_by((Question.count1 + Question.count2).desc()).limit(5).all()
#     question = db.session.query(Question).order_by(func.random()).paginate(per_page=10, page=page)
#     return render_template("index.html",question = question,trending = trending)


# @app.route("/add_ques", methods=['GET', 'POST'])
# def add_ques():
#     form = QuestionForm()
#     if form.validate_on_submit():
#         ques = Question(question = form.question.data,option1 = form.option1.data,\
#                         option2 = form.option2.data)
#         db.session.add(ques)
#         db.session.commit()
#         flash(f"Question has been added", 'success')
#         return redirect(url_for('home'))
#     return render_template("add_question.html",form = form)
# @app.route("/vote/<int:question_id>/<option>")
# def vote(question_id, option):
#     question = Question.query.get_or_404(question_id)
#     if option == 'option1':
#         question.count1 += 1
#     elif option == 'option2':
#         question.count2 += 1
#     else:
#         return abort(404)
#     db.session.commit()
#     flash('Your vote has been recorded.', 'success')
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True)


