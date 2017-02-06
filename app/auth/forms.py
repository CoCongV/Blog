# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from app.models.users import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password2', message='请确认两次密码是否一致')])
    submit = SubmitField('登录')


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('username', validators=[DataRequired(), Length(1, 32)])
    password = PasswordField('password', validators=[DataRequired(), Length(6, 20), EqualTo('password2')])
    password2 = PasswordField('password2', validators=[DataRequired(), Length(6, 20)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return ValidationError('邮箱已被使用')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return ValidationError('用户名已被使用')

class PostForm(Form):
    Title = StringField()