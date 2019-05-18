from flask import current_app, render_template
from flask_mail import Message

from blog import mail, celery

def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['FLASK_MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
