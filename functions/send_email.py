import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendEmail:

    def __init__(self, receiver_email, subject, message_html):
        self.sender_email = os.environ['SENDER_EMAIL']
        self.sender_password = os.environ['SENDER_PASSWORD']
        self.receiver_email = receiver_email
        self.subject = subject
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


