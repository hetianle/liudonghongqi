from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm
from app.forms import ExampleForm, LoginForm
from app.models import User


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/list/')
def posts():
	return render_template('list.html')


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
    if g.user is not None and g.user.is_authenticated:
        flash('login successed')
        return redirect(url_for('index'))
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
        return redirect(url_for('login'))
					
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

# ====================
