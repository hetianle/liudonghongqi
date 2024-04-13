from app import db
from sqlalchemy import Enum

class ModelExample(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(250))
	content = db.Column(db.Text)
	date = db.Column(db.DateTime)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(500))
    identity = db.Column(Enum('老师', '学生'))

    # name = db.Column(db.String(500))
    # email = db.Column(db.String(120), unique = True)
    # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, unique = True)
    level = db.Column(db.Integer)
    # tag = db.Column(
    #     db.String(64),
    candidate_answers = db.Column(db.JSON)
    correct_answer = db.Column(db.String(1))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'level': self.level,
            'candidate_answers': self.candidate_answers,
            'correct_answer': self.correct_answer
        }
    
class SelectedQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False, unique=True)
    grade = db.Column(db.Float, nullable=False)
    # answers =db.Column(db.String(80))