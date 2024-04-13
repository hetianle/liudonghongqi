
from app.models import User
from app.models import Question,SelectedQuestion
from app import db

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

def clear_all_selected_questions():
    questions = SelectedQuestion.query.all()
    for question in questions:
        db.session.delete(question)
    db.session.commit()
    # print(f"Num Selected Questions:{len(questions)}")
    return questions


def query_questions_by_ids(ids):
    if not isinstance(ids, list):
        ids = [ids]
    results = []
    for id in ids:
        question = Question.query.get(id)
        results.append(question.to_dict())
    return results 



def insert_init_questions():
    questions = [
        {'title': 'Question 1', 'level': 'Easy'},
        {'title': 'Question 2', 'level': 'Medium'},
        {'title': 'Question 3', 'level': 'Hard'},
        {'title': 'Question 4', 'level': 'Easy'},
        {'title': 'Question 5', 'level': 'Medium'},
        {'title': 'Question 6', 'level': 'Hard'},
        # Add more questions as needed
    ]

    for question_data in questions:
        question = Question(title=question_data['title'], level=question_data['level'])
        db.session.add(question)
    db.session.commit()