# coding: utf-8
from flask import flash
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

from app.models.roles import Role
from app.models.users import User


class EditProfileForm(Form):
    username = StringField('用户名', validators=[Length(0, 32)])
    location = StringField('地区', validators=(Length(0, 64)))
    about_me = TextAreaField('关于自己', validators=(Length(0, 128)))
    submit = SubmitField('Submit')

    def validate_username(self, field):
        user = User.query.filter_by(username=field).first()
        if user is not None:
            return ValidationError('用户名已被使用')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1,64)])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于自己', validators=[Length(0, 128)])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.all().order_by(Role.name)]
        self.user = user

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if field.data != self.user.email and user:
            raise ValidationError('Email 已经被使用')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if field.data != self.user.username and user:
            raise ValidationError('用户名已经被使用')

class PostForm(Form):
    title = StringField('标题', validators=[DataRequired(), Length(1, 32)])
    body = PageDownField(validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = TextAreaField('评论', validators=[Length(1, 1000)])
    submit = SubmitField('Submit')