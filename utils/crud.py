
from app.models import User
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



def init_question_databse():
    questions = [
        {'title': 'Question 1', 'level': 'Easy', 'answer': 'A', 'choices':''},
        {'title': 'Question 2', 'level': 'Medium', 'answer': 'A', 'choices':''},
        {'title': 'Question 3', 'level': 'Hard', 'answer': 'A', 'choices':''},
        {'title': 'Question 4', 'level': 'Easy', 'answer': 'A', 'choices':''},
        {'title': 'Question 5', 'level': 'Medium', 'answer': 'A', 'choices':''},
        {'title': 'Question 6', 'level': 'Hard', 'answer': 'A', 'choices':''},
        {'title': 'Question 1', 'level': 'Easy', 'answer': 'A', 'choices':''},
        {'title': 'Question 2', 'level': 'Medium', 'answer': 'A', 'choices':''},
        {'title': 'Question 3', 'level': 'Hard', 'answer': 'A', 'choices':''},
        {'title': 'Question 4', 'level': 'Easy', 'answer': 'A', 'choices':''},
        {'title': 'Question 5', 'level': 'Medium', 'answer': 'A', 'choices':''},
        {'title': 'Question 7777', 'level': 'Hard', 'answer': 'A', 'choices':''},
        # Add more questions as needed
    ]
    questions = [
        {'title': '上海面积最大的区是哪个？', 'level': 'Easy', 'candidate_answers': {'A': '浦东新区', 'B': '青浦区', 'C': '松江区', 'D': '嘉定区'}, 'correct_answer': 'A'},
        {'title': '下面四个城市与上海接壤的城市是哪个', 'level': 'Easy', 'candidate_answers': {'A': '苏州', 'B': '杭州', 'C': '南京', 'D': '无锡'}, 'correct_answer': 'A'},
        {'title': '抗日战争时期下面哪场战役发生在上海？',   'level': 'Easy', 'candidate_answers': {'A': '淞沪会战', 'B': '平型关战役', 'C': '台儿庄战役', 'D': '百团大战'}, 'correct_answer': 'A'},
        {'title': '淞沪会战后期为什么在中国军队几乎完全撤离的情况下仍然要守护四行仓库？', 'level': 'Hard', 'candidate_answers': {'A': '为了保护列强的资产', 'B': '为了向列强证明中国仍然在抵抗为了维护中国的尊严', 'C': '为了守护坚固据点等待援军反击', 'D': '为了保护上海的工业'}, 'correct_answer': 'B'},

    ]

    for question_data in questions:
        question_query = Question.query.filter_by(title=question_data['title']).first()
        if question_query is None:
            question = Question(title=question_data['title'], level=question_data['level'], candidate_answers=question_data['candidate_answers'], correct_answer=question_data['correct_answer'])
            db.session.add(question)
    db.session.commit()


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



def clear_db_data(model):
    db.session.query(model).delete()
    db.session.commit()
    print(f"Clear table {model.__name__} done")