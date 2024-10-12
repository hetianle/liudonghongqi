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
from app.models import EvaluationItem, EvaluationDimension, EvaluationResult
from app.models import User, ClassName

from datetime import datetime
import pytz

# Set the time as Beijing time
beijing_tz = pytz.timezone('Asia/Shanghai')

from django.shortcuts import render
from .models import EvaluationItem
import json

def evaluation_view(request):
    evaluation_items = EvaluationItem.objects.all()
    evaluation_items_dict = [item.to_dict() for item in evaluation_items]
    context = {
        'evaluation_items': json.dumps(evaluation_items_dict)
    }
    return render(request, 'evaluation.html', context)

@app.route('/evaluation_settings', methods=['GET', 'POST'])
def evaluation_settings():
    # if currenct user's role is not admin 
    if g.user.identity != UserRole.ADMINISTRATOR:
        flash('暂无权限', 'warning')
        return render_template('base.html', user=g.user)  # Assuming you have a blank.html template
    
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        dimension_names = request.form.get('dimension_names')
        # admin_user_id = request.form.get('admin_user_id')
        evaluator_ids = request.form.getlist('evaluators')
        class_ids = request.form.getlist('classes')
        admin_user_id = current_user.id
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        loop_rule = request.form.get('evaluation_loop')
        # if item_name and dimension_names:
        #     for dimension_name in dimension_names.split(' '):
        #         new_dimension = EvaluationDimension(name=dimension_name)
        #         db.session.add(new_dimension)

        if item_name and dimension_names:
            new_item = EvaluationItem(name=item_name, admin_user_id=admin_user_id, )
            if evaluator_ids:
                for evaluator_id in evaluator_ids:
                    evaluator_user = User.query.get(evaluator_id)
                    if evaluator_user:
                        new_item.evaluators.append(evaluator_user)
            if class_ids:
                for class_id in class_ids:
                    class_name = ClassName.query.get(class_id)
                    if class_name:
                        new_item.evaluate_classes.append(class_name)
            if dimension_names:
                for dimension_name in dimension_names.split(' '):
                    diname = EvaluationDimension.query.get(dimension_name)
                    if diname:
                        new_item.dimensions.append(diname)
                    else:
                        # insert the input diname into EvaluationDimension db
                        new_dimension = EvaluationDimension(name=dimension_name, item_name=new_item.name)
                        db.session.add(new_dimension)
                        db.session.commit()
                        new_item.dimensions.append(new_dimension)
            
            if start_date and end_date and loop_rule:
                # print(start_date,'--------------------------------------------------------')
                new_item.start_date = datetime.strptime(start_date, "%Y-%m-%d")
                new_item.end_date = datetime.strptime(end_date, "%Y-%m-%d")
                new_item.loop_rule = loop_rule
            
            
            db.session.add(new_item)
            db.session.commit()

            db.session.commit()
            return redirect(url_for('evaluation_settings'))

    items = EvaluationItem.query.all()
    evaluators = User.query.all()
    classes = ClassName.query.all()
    return render_template('evalsettings.html', user=g.user, items=items, evaluators= evaluators, classes=classes)


@app.route('/evaluation', methods=['GET', 'POST'])
def evaluation():
    evaluation_items = EvaluationItem.query.all()
    context = {}
    evaluation_items_dict = [item.to_dict() for item in evaluation_items]
    # print(f"evaluation_items_dict:----------------------------------\n{evaluation_items_dict}")
    context.update({
        'evaluation_items': json.dumps(evaluation_items_dict, ensure_ascii=False)
    })
    if request.method == 'POST':
        beijing_tz = pytz.timezone('Asia/Shanghai')
        for item in evaluation_items:
            evaluators = item.evaluators
            if g.user in evaluators:
                for class_ in item.evaluate_classes:
                    for dimension in item.dimensions:
                        score = request.form.get(f'score_{item.id}_{class_.id}_{dimension.id}')
                        if score:
                            evaluation_result = EvaluationResult(
                                evaluation_item_id=item.id,
                                user_id=g.user.id,
                                dimension_id=dimension.id,
                                class_id=class_.id,
                                grade=float(score),
                                time=datetime.now(beijing_tz)
                            )
                            db.session.add(evaluation_result)
        db.session.commit()
        flash('Evaluation results saved successfully!', 'success')
        return redirect(url_for('evaluation'))

    return render_template('evaluation.html', user=g.user, evaluation_items=evaluation_items, evaluation_items_context = json.dumps(evaluation_items_dict, ensure_ascii=False))

@app.route('/evaluation_results', methods=['GET'])
def evaluation_results():
    # Query all evaluation results from the database
    results = EvaluationResult.query.all()
    
    # Render the evaluation_results.html template with the retrieved results
    return render_template('evaluation_results.html', results=results, user=g.user)

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
