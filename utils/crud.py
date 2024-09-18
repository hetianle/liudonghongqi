
from app.models import User, ClassName
# from app.models import Question,SelectedQuestion,Grade, UserRole
from app import db
from app.models import UserRole

def query_all_users():
    users = User.query.all()
    for user in users:
        print(user.id,  user.user, '   ' , user.password)

def query_all_questions():
    questions = Question.query.all()
    for question in questions:
        print(question.id,  question.title, '   ' , question.level)
    return questions

def query_all_selected_questions():
    questions = SelectedQuestion.query.all()
    print(f"Num Selected Questions:{len(questions)}")
    for question in questions:
        print(f"selected question db: questionid:{question.question_id}  userid:{question.user_id}")
    return questions

# def clear_all_selected_questions():
#     questions = SelectedQuestion.query.all()
#     for question in questions:
#         db.session.delete(question)
#     db.session.commit()
#     # print(f"Num Selected Questions:{len(questions)}")
#     return questions

def clear_all_grades():
    grades = Grade.query.all()
    for grade in grades:
        db.session.delete(grade)
    db.session.commit()
    # print(f"Num Selected Questions:{len(questions)}")
    return grades


def query_questions_by_ids(ids):
    if not isinstance(ids, list):
        ids = [ids]
    results = []
    for id in ids:
        question = Question.query.get(id)
        results.append(question.to_dict())
    return results 


def init_user_databse():
    init_users = [
        {'user': 'admin1', 'password': '123', 'identity':  UserRole.ADMINISTRATOR},
        {'user': 'admin2', 'password': '123', 'identity': UserRole.ADMINISTRATOR},
        {'user': 'eval1', 'password': '123', 'identity': UserRole.EVALUATOR},
        {'user': 'eval2', 'password': '123', 'identity': UserRole.EVALUATOR},
        {'user': 'eval3', 'password': '123', 'identity': UserRole.EVALUATOR},
        {'user': 'eval4', 'password': '123', 'identity': UserRole.EVALUATOR},
    ]
    for user_data in init_users:
        user = User.query.filter_by(user=user_data['user']).first()
        if user is None:
            user = User(user=user_data['user'], password=user_data['password'], identity=user_data['identity'])
            db.session.add(user)
    db.session.commit()


def init_classname_database():
    init_classes = [
        {'name': 'class1'},
        {'name': 'class2'},
        {'name': 'class3'},
        {'name': 'class4'},
    ]
    for class_data in init_classes:
        class_name = ClassName.query.filter_by(name=class_data['name']).first()
        if class_name is None:
            class_name = ClassName(name=class_data['name'])
            db.session.add(class_name)
    db.session.commit()

def clear_db_data(model):
    db.session.query(model).delete()
    db.session.commit()
    print(f"Clear table {model.__name__} done")