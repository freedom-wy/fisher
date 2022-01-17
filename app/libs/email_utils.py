"""
发送邮件
"""
from flask_mail import Message
from flask import current_app, render_template
# from app import mail
from threading import Thread
from flask_mail import Mail

mail = Mail()


# 异步发送邮件
def async_send_email(app, msg):
    with app.app_context():
        mail.send(msg)


def handle_send_mail(to, subject, template, **kwargs):
    msg = Message(subject="[鱼书]{}".format(subject), sender=current_app.config.get("MAIL_USERNAME"), recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    t = Thread(target=async_send_email, args=(app, msg))
    t.start()


if __name__ == '__main__':
    from app import create_app

    app = create_app()
    with app.app_context():
        handle_send_mail()
