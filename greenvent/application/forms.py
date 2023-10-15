from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from application.models import user


class  RegisterForm(FlaskForm):

    def validate_uname(self,utc):
        u=user.query.filter(user.uname==utc.data).first()
        if u and (u.role=='manager'):
            raise ValidationError('Manager already exists!')     
        if u and (u.role=='User'):
            raise ValidationError('User already exists!') 

    uname=StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    password1=PasswordField(label='password:', validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='confirm password:', validators=[EqualTo('password1'),DataRequired()])
    mancode=StringField(label='Manager Code:')
    submit=SubmitField(label='create account')

class LoginForm(FlaskForm):
        
    uname=StringField(label='User Name:',validators=[DataRequired()])
    password=PasswordField(label='password:', validators=[DataRequired()])
    submit=SubmitField(label='login')


