from email.mime.text import MIMEText


async def send_eamil(app, to, subject, template):
    message = MIMEText('Sent via aiostmplib')
    message['From'] = app.config['BLOG_ADMIN']
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(template, 'html', 'utf8'))
    await app.smtp.send_message(message)
