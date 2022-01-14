"""
发送邮件
"""
from flask_mail import Message
from flask import current_app, render_template
from app import mail


def handle_send_mail(to, subject, template, **kwargs):
    msg = Message(subject="[鱼书]{}".format(subject), sender=current_app.config.get("MAIL_USERNAME"), recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        handle_send_mail()
