import os
from celery import Celery
from celery.schedules import crontab

from functions.db import User
from functions.send_email import SendEmail, send_stats

user = os.environ.get('RABBITMQ_DEFAULT_USER')
psd = os.environ.get('RABBITMQ_DEFAULT_PASS')
host = 'rabbit_mq'

celery = Celery('celery_task', broker=f'''pyamqp://{user}:{psd}@{host}//''')
celery.conf.beat_schedule = {
    'send_stats_task_every_minute': {
        'task': 'celery_task.send_stats_task',
        'schedule': crontab(minute='*'),
    },
}


@celery.task
def send_mail(email_data):
    with SendEmail(**email_data) as email:
        return email.send()

@celery.task
def send_stats_task():
    send_stats(User.query.filter_by(id=2).first())


