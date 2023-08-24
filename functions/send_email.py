import os
import secrets
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template

from functions.db import User, get_or_create, UserVerification, db_session


class SendEmail:

    def __init__(self, receiver_email, subject, message_html):
        self.sender_email = os.environ['SENDER_EMAIL']
        self.sender_password = os.environ['SENDER_PASSWORD']
        self.receiver_email = receiver_email
        self.subject = subject.strip() + ' | Вилки-Палки'
        self.message_html = message_html

        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.server.login(self.sender_email, self.sender_password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()

    def send(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.message_html, 'html', 'UTF-8'))

        try:
            self.server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            return True
        except Exception as ex:
            return False


def send_verification_code(user: User):

    user_verify = get_or_create(UserVerification, filters=dict(user_id=user.id))
    user_verify.code = secrets.token_hex(3)
    user_verify.timestamp = datetime.fromtimestamp(time.time())
    db_session.commit()

    email_data = dict(
        subject='Подтверждение почты',
        receiver_email=user.email,
        message_html=render_template('email_verification.html', code=user_verify.code),
    )
    with SendEmail(**email_data) as email:
        is_send = email.send()