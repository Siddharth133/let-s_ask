from extensions import db
from datetime import datetime

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    count1 = db.Column(db.Integer, nullable=False,default = 0)
    count2 = db.Column(db.Integer, nullable=False,default = 0)
    

    def __repr__(self):
        return f"Post('{self.question}','{self.date_posted}')"