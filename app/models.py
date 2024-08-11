from app import db
from sqlalchemy import Enum

class UserRole(Enum):
    ADMINISTRATOR = "administrator"
    EVALUATOR = "evaluator"
    SUBSCRIBER = "subscriber"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(500))
    identity = db.Column(Enum(UserRole.ADMINISTRATOR, UserRole.EVALUATOR, UserRole.SUBSCRIBER))

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



class EvaluationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dimensions = db.relationship('EvaluationDimension', backref='item', lazy=True)

class EvaluationDimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('evaluation_item.id'), nullable=False)