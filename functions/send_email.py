import os
import secrets
import smtplib
import time
from datetime import datetime, date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pdfkit
from flask import render_template

from config import app_config
from functions.db import User, get_or_create, UserVerification, db_session
from functions.stats import get_stats


class SendEmail:

    def __init__(self, receiver_email, subject, message_html, attachments=[]):
        self.sender_email = os.environ['SENDER_EMAIL']
        self.sender_password = os.environ['SENDER_PASSWORD']
        self.receiver_email = receiver_email
        self.subject = subject.strip() + ' | Вилки-Палки'
        self.message_html = message_html
        self.attachments = attachments

        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
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

        if self.attachments:
            for attachment in self.attachments:
                msg.attach(attachment)

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


def send_stats(user: User, day=date.today()):

    email_data = dict(
        subject=f'Статистика за {day}',
        receiver_email=user.email,
        message_html=render_template('stats.html', **get_stats(day)),
    )
    path = os.path.join(app_config.get('UPLOAD_FOLDER'), str(day)+'.pdf')
    pdf = pdfkit.from_string(email_data['message_html'], path)

    with open(path, 'rb') as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
        pdf_attachment.add_header(
            'content-disposition', 'attachment', filename=f'''{email_data['subject']}.pdf'''
        )

    with SendEmail(**email_data, attachments=[pdf_attachment]) as email:
        email.send()