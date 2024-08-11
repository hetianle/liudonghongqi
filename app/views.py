from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm
from app.forms import ExampleForm, LoginForm
from app.models import User, UserRole
from flask import request
# from utils.crud import  query_all_questions,  query_questions_by_ids, query_all_selected_questions, clear_all_selected_questions
from app import db
from flask import jsonify
# from app.models import User, Question, SelectedQuestion, Grade
from app.models import EvaluationItem, EvaluationDimension


@app.route('/evaluation_settings', methods=['GET', 'POST'])
def evaluation_settings():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        dimension_names = request.form.getlist('dimension_names')

        if item_name and dimension_names:
            new_item = EvaluationItem(name=item_name)
            db.session.add(new_item)
            db.session.commit()

            for dimension_name in dimension_names:
                new_dimension = EvaluationDimension(name=dimension_name, item_id=new_item.id)
                db.session.add(new_dimension)

            db.session.commit()
            return redirect(url_for('evaluation_settings'))

    items = EvaluationItem.query.all()
    return render_template('evalsettings.html', user=g.user, items=items)



@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        if g.user.identity == UserRole.ADMINISTRATOR:
            return render_template('index.html', user = g.user)
        else:
            return render_template('index.html',  user = g.user)
    else:
        return redirect(url_for('login'))

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
        flash('User Save User name')
        return redirect(url_for('index'))
    else:
        print(f"Not login yet")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.user.data).first()
        if user is None or user.password != form.password.data:
            flash('用户名或密码错误','error')
            return redirect(url_for('login'))
        else:
            flash('登录成功')
            login_user(user, remember=True)
            return redirect(url_for('index'))
    else:
        print(f"USER VALIDATE FAILED")
        return render_template('login.html', user=g.user, form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('login')) 
# ====================
