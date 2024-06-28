from __future__ import absolute_import, unicode_literals
import eventlet
eventlet.monkey_patch()

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('djangoProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-news-every-minute': {
        'task': 'news_aggregator.tasks.update_news',
        'schedule': crontab(minute='*/2'),
    },
}
