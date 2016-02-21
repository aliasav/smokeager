from celery.task.schedules import crontab  
from celery.decorators import periodic_task, task
from smoker.models import Smoker, SmokeAnalytic
import datetime, logging

logger = logging.getLogger(__name__)

@periodic_task(run_every=crontab(minute=0, hour=0))
def reset_daily_count():
    smoker_analytics = SmokeAnalytic.objects.all()
    for sa in smoker_analytics:
        sa.daily_count = 0
        sa.save()
        logger.debug("Reset daily count: %s" %sa)


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_week="sunday"))
def reset_weekly_count():
    smoker_analytics = SmokeAnalytic.objects.all()
    for sa in smoker_analytics:
        sa.weekly_count = 0
        sa.save()
        logger.debug("Reset weekly count: %s" %sa)