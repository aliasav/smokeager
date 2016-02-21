from __future__ import absolute_import
from kombu import Exchange, Queue
from celery import Celery
from django.conf import settings
import os

smoekager = Celery('smoekager',
             broker="amqp://autobot:autobot@localhost:5672",
)

# Optional configuration, see the application user guide.
smoekager.conf.update(
    CELERY_TASK_RESULT_EXPIRES=100, # May cause memory leak
)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoekager.celeryconfig')

#.config_from_object('smoekager.celeryconfig', silent=False)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
#smoekager.config_from_object('django.conf:settings')
smoekager.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@smoekager.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

if __name__ == '__main__':
    smoekager.start()
