from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm
from app.forms import ExampleForm, LoginForm
from app.models import User, Question, SelectedQuestion, Grade, UserRole
from flask import request
from utils.crud import  query_all_questions,  query_questions_by_ids, query_all_selected_questions, clear_all_selected_questions
from app import db
from flask import jsonify
# from app.models import User, Question, SelectedQuestion, Grade

@app.route('/leaderboard')
def leaderboard():
    grades = Grade.query.order_by(Grade.grade.desc()).all()
    return render_template('leaderboard.html', grades=grades)

@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        # flash('login successed')
        if g.user.identity == UserRole.ADMINISTRATOR:
            return render_template('index.html')
        else:
            selected_questions_id = SelectedQuestion.query.all()
            

            selected_questions_id = [sid.question_id for sid in selected_questions_id]

            print(f"Student got: {len(selected_questions_id)} questions. {selected_questions_id}")

            selected_questions = query_questions_by_ids(selected_questions_id)

            return render_template('index_stu.html', selected_questions=selected_questions)
    else:
        return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    print(f'------------------- student submit----------------')
    data = request.get_json(force=True)
    print(f'------------------- student submit parse complete ----------------')
    answers = data['userAnswers']
    grade =data['grade']
    # print(f'username:{g.user.user} grade:{grade} answers:{answers}')
    # submited_grades = Grade.query.all()
    # for grade_ins in submited_grades:
    submited_temp_user = Grade.query.filter_by(user=g.user.user).all()
    if len(submited_temp_user) > 0:
        flash('已经提交过了')
        print('已经提交过了')
        return redirect(url_for('index'))
    else:
        temp_user_grade = Grade(user=g.user.user, grade=grade)
        db.session.add(temp_user_grade)
        db.session.commit()
        submited_temp_user = Grade.query.filter_by(user=g.user.user).all()
        if len(submited_temp_user) > 0: 
            flash('提交成功')
            print('提交成功')
        else:
            flash('提交失败')
            print('提交失败')
        return redirect(url_for('index'))

         
    # return redirect(url_for('index'))


@app.route('/list/')
def list():
    question_type = request.args.get('question_type')
    questions = query_all_questions()
    return render_template('list.html', question_type= question_type, questions=questions)

@app.route('/submit_selections', methods=['POST'])
def submit_selections():
    last_res = query_all_selected_questions()
    if len(last_res) > 0:
        message = f"已经有{len(last_res)}道题发送到学生，请先终止答题"
        flash(message=message)
        return redirect(url_for('list'))

    selected_question_ids = request.form.getlist('question')
    user_id = current_user.id  # replace with your actual user ID

    selected_questions = query_questions_by_ids(selected_question_ids)
    for question in selected_questions:
        selected_question = SelectedQuestion(question_id=question['id'], user_id=user_id)
        db.session.add(selected_question)
    db.session.commit()

    res = query_all_selected_questions()
    message = f"已将{len(res)}道题发送到学生"
    flash(message=message)

    return redirect(url_for('list'))

@app.route('/end', methods=['GET'])
def end():
    user_id = current_user.id  # replace with your actual user ID

    # Query all selected questions for the current user
    selected_questions = SelectedQuestion.query.filter_by(user_id=user_id).all()

    # Delete all selected questions
    for question in selected_questions:
        db.session.delete(question)

    db.session.commit()

    flash('已终止答题')
    return redirect(url_for('list'))

@app.route('/new/')
@login_required
def new():
	form = ExampleForm()
	return render_template('new.html', form=form)


@app.route('/save/', methods = ['GET','POST'])
@login_required
def save():
	form = ExampleForm()
	if form.validate_on_submit():
		print("salvando os dados:")
		print(form.title.data)
		print(form.content.data)
		print(form.date.data)
		flash('Dados salvos!')
	return render_template('new.html', form=form)

@app.route('/view/<id>/')
def view(id):
	return render_template('view.html')

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    print(f"Get into login route")
    if g.user is not None and g.user.is_authenticated:
        flash('login successed')
        return redirect(url_for('index'))
    else:
        print(f"Not login yet")

    form = LoginForm()
    if form.validate_on_submit():
        print(f"USER VALIDATE SuCCESSfull   active:{g.user.is_active}")

        user = User.query.filter_by(user=form.user.data).first()
        if user is None or not user.password == form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            flash('login successed')
            login_user(user, remember=True)
            return redirect(url_for('index'))
    else:
        print(f"USER VALIDATE FAILED")
        return render_template('login.html', form=form)
					
# @app.route('/logout/')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index')) 
# ====================
