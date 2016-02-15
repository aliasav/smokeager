"""
generic utilties to be used
"""

import json, string, logging, datetime, pytz
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.utils.timezone import utc
from smoker.models import Smoke, SmokeGroup

logger = logging.getLogger(__name__)


"""
Function that fetches user and smoker object from a token key.
Returns None if not found
This promotes DRY in handling all user/smoker objects not found cases
"""
def get_user_smoker_from_token(token_key):

    # fetch token object
    try:
        token = Token.objects.get(key=token_key)
    except:
        logger.exception("Token object does not exist for key: %s" %token_key)
        return (None, None)

    # token found, process to fetch user
    else:
        logger.info("Token found for key %s: %s" %(token_key, token))
        try:
            user = token.user
        except:
            logger.exception("Error in getting user for token: %s" %token)
            return (None, None)

        # user found, proceed to fetch smoker
        else:
            logger.info("User found for token key %s: %s" %(token, user))
            try:
               smoker = user.smoker
            except:
                logger.exception("Error in gettingsmoker from user %s." %user)
            else:
                logger.info("Customer found for user %s: %s" %(user, smoker))
                # user and smoker successfully fetched from token
                return (user, smoker)


# fetches analytics data for user
# user/smoker is required as input
def fetch_smoker_analytics(user=None, smoker=None):

    #logger.debug("fetch_smoker_analytics user: %s \tsmoker: %s" %(user, smoker))
    resp_data = None; s = None;

    if user:        
        try:
            s = user.smoker
        except:
            logger.exception("Error in fetching smoker for user: %s" %user)
            resp_data = None
    elif smoker:
        s = smoker
    else:
        resp_data = None

    if s:
        analytics_obj = s.smoke_analytic_individual
        resp_data = {
            "total count": analytics_obj.smoke_count,
            "daily count": analytics_obj.daily_count,
            "weekly count": analytics_obj.weekly_count,
            "monthly count": analytics_obj.monthly_count,
            "time since last smoke": last_smoke(analytics_obj, s),
            "longest break": longest_break(s),
        }

    else:
        resp_data = None

    #logger.debug("fetch_smoker_analytics resp_data: %s" %resp_data)
    return resp_data

# takes a timedelta object and returns human readable format
def convert_time_diff_to_string(time_diff):
    time_diff_hours = time_diff.seconds/3600
    m1 = time_diff.seconds%3600
    time_diff_minutes = m1/60
    time_diff_secs = m1%60
    time_diff_string = str(time_diff_hours) + " hours " + str(time_diff_minutes) + " minutes " \
                        + str(time_diff_secs) + " seconds"
    return time_diff_string

# calculates time since last smoke
def last_smoke(analytics_obj, smoker):
    current_time = datetime.datetime.now(pytz.utc)
    latest_time = Smoke.objects.filter(smokers=smoker).latest("created_at").created_at
    latest_time = latest_time.replace(tzinfo=pytz.utc)
    time_diff_string = convert_time_diff_to_string(current_time-latest_time)
    return time_diff_string


# calculates longest break
def longest_break(smoker):
    # get all smoke times
    smoke_times = Smoke.objects.filter(smokers=smoker)
    smoke_times = map(lambda x: x.created_at, smoke_times)

    if len(smoke_times)>=2:
        d = None; D = abs(smoke_times[1] - smoke_times[0]);
        for i in xrange(0, len(smoke_times)-2):
            d = abs(smoke_times[i+1] - smoke_times[i])
            if (d > D):
                D = d
        D = convert_time_diff_to_string(D)
    else:
        D = None

    return D

# creates a smoke group
def create_smoke_group(data):

    # get admin smoker for group
    try:
        user, admin = get_user_smoker_from_token(data["token"])
    except:
        logger.exception("Error in fethcing smoker/user for key: %s" %data["token"])
    else:
        if admin:
            # create group
            group = SmokeGroup.objects.create(admin=admin, name=data["group_name"], password=data["group_password"])
            group.smokers.add(admin)
            group.save()
            logger.debug("Smoke group created: %s" %smoke_group)
            return group

        else:
            return None


