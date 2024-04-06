from flask_wtf import FlaskForm
from wtforms  import StringField, TextAreaField, DateTimeField, PasswordField,BooleanField
from wtforms.validators import DataRequired

class ExampleForm(FlaskForm):
	title = StringField(u'Título', validators = [DataRequired()])
	content = TextAreaField(u'Conteúdo')
	date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(FlaskForm):
	user = StringField(u'用户名', validators = [DataRequired()])
	password = PasswordField(u'密码', validators = [DataRequired()])
	remember_me = BooleanField('下次自动登录')
