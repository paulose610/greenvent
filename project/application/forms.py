from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from application.models import user


class  RegisterForm(FlaskForm):

    def validate_uname(self,utc):
        u=user.query.filter(user.uname==utc.data).first()
        if u and (u.role=='user'):
            raise ValidationError('Username already exists!')    

    uname=StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    password1=PasswordField(label='password:', validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='confirm password:', validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='create account')

class LoginForm(FlaskForm):
    """def validate_uname(self,utl):
        u=user.query.filter(user.uname==utl.data).first()
        p=user.query.filter(user.pswdhash==utl.data).first()
        if not u or not p:
            raise ValidationError('Username or Password is wrong!')"""
        
    uname=StringField(label='User Name:',validators=[DataRequired()])
    password=PasswordField(label='password:', validators=[DataRequired()])
    submit=SubmitField(label='login')