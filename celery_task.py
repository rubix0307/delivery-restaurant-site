import os
from celery import Celery
from functions.send_email import SendEmail

user = os.environ.get('RABBITMQ_DEFAULT_USER')
psd = os.environ.get('RABBITMQ_DEFAULT_PASS')
host = 'rabbit_mq'
celery = Celery('celery_task', broker=f'''pyamqp://{user}:{psd}@{host}//''')


@celery.task
def send_mail(email_data):
    with SendEmail(**email_data) as email:
        return email.send()