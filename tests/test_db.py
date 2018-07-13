import unittest
from blog import create_app, db
from blog.models import User, Role, AnonymousUser, Permission, Post, Comment


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_register(self):
        role = Role.query.filter_by(name='Administrator').first()
        user = User.create(username='moon',
                           email='cong.lv.yx@gamil.com',
                           password='password',
                           role=role,
                           confirmed=True,
                           about_me='Python爱好者'
                           )
        user.to_json()
        token = user.generate_confirm_token(expiration=86400)
        email_token = user.generate_email_token()
        user.is_administrator()
        user.verify_auth_token(token)
        user.verify_email_token(email_token)

        password_token = user.generate_reset_token()
        user.verify_reset_token(password_token, 'password')

        change_email_token = user.generate_change_mail_token(
            new_email='cong.lv.yx@gamil.com')
        user.verify_change_mail(change_email_token)

    def test_add_user(self):
        role = Role.query.filter_by(name='Administrator').first()
        user = User.create(username='moon1',
                           email='cong.lv.yx1@gamil.com',
                           password='password',
                           role=role,
                           confirmed=True,
                           about_me='Python')
        db.session.add(user)
        db.session.commit()
        user.json()

    def test_anonymousUser(self):
        user = AnonymousUser()
        user.can(Permission.COMMENT)
        user.is_administrator()
        user.is_anonymous()


class TestPostModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.user = self.register_user()
        self.post = self.add_post()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self):
        role = Role.query.filter_by(name='Administrator').first()
        user = User.create(username='moon',
                           email='cong.lv.yx@gamil.com',
                           password='password',
                           role=role,
                           confirmed=True,
                           about_me='Python爱好者'
                           )
        return user

    def add_post(self):
        post = Post.create(title='test',
                           body='test body',
                           tags=['test', '测试'],
                           author=self.user)
        db.session.add(post)
        db.session.commit()
        post.to_json(True)
        post.to_json()
        post.generate_fake()
        return post

    def test_comment(self):
        comment = Comment.create(body='test',
                                 author=self.user,
                                 post=self.post)
        print(comment)
        comment.to_json()
        reply = Comment.create(body='reply',
                               author=self.user,
                               post=self.post)
        reply.reply(comment)
