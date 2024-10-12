from app import db
from sqlalchemy import Enum
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import datetime

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
        return self.user

# class ClassName(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(64), unique = True)
class ClassName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Foreign key to EvaluationItem
    evaluation_item_id = db.Column(db.Integer, db.ForeignKey('evaluation_item.id'))
    # def __str__(self):
    #     return self.name
    def __repr__(self):
        return self.name


# Association table for the many-to-many relationship between EvaluationItem and User (evaluators)
evaluation_evaluators = Table('evaluation_evaluators', db.Model.metadata,
    Column('evaluation_id', Integer, ForeignKey('evaluation_item.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class EvaluationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # One-to-many relationship with EvaluationDimension
    dimensions = db.relationship('EvaluationDimension', backref='item', lazy=True)
    
    # One-to-one relationship with admin User
    admin_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_user = db.relationship('User', foreign_keys=[admin_user_id], backref='admin_items', lazy=True)
    
    # Many-to-many relationship with evaluator Users
    evaluators = db.relationship('User', secondary=evaluation_evaluators, backref='evaluated_items', lazy=True)
    
    # One-to-many relationship with ClassName
    evaluate_classes = db.relationship('ClassName', backref='item', lazy=True)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    loop_rule = db.Column(Enum('monthly', 'weekly', 'daily', name='loop_rule'), nullable=False)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dimensions': [dimension.to_dict() for dimension in self.dimensions],
        }
    
    
class EvaluationDimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_name = db.Column(db.Integer, db.ForeignKey('evaluation_item.name'), nullable=False)
    def __repr__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            # Add other fields as necessary
        }
    
    
class EvaluationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to EvaluationItem
    evaluation_item_id = db.Column(db.Integer, db.ForeignKey('evaluation_item.id'), nullable=False)
    evaluation_item = db.relationship('EvaluationItem', backref='evaluation_results', lazy=True)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='evaluation_results', lazy=True)
    
    # Foreign key to EvaluationDimension
    dimension_id = db.Column(db.Integer, db.ForeignKey('evaluation_dimension.id'), nullable=False)
    dimension = db.relationship('EvaluationDimension', backref='evaluation_results', lazy=True)
    
    # Foreign key to Class
    class_id = db.Column(db.Integer, db.ForeignKey('class_name.id'), nullable=False)
    class_ = db.relationship('ClassName', backref='evaluation_results', lazy=True)
    
    
    # Grade field
    grade = db.Column(db.Float, nullable=False)
    
    # Time field
    time = db.Column(db.DateTime, default=datetime.date, nullable=False)

    def __repr__(self):
        return f'<EvaluationResult {self.id}>'