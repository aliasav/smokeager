"""
generic utilties to be used
"""

import json, string, logging, datetime, pytz
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.utils.timezone import utc
from smoker.models import Smoke, SmokeGroup
from django.conf import settings

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
            #"daily count": analytics_obj.daily_count,
            #"weekly count": analytics_obj.weekly_count,
            #"monthly count": analytics_obj.monthly_count,
            "time since last smoke": last_smoke(analytics_obj, s),
            "last 3 smokes": last_3_smokes(analytics_obj, s),
            "longest break": longest_break(s),
            "amount spent": "Rs." + str(amount_spent(analytics_obj, s)),
            "past days records": past_days_smokes(analytics_obj, s),
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
    try:
        latest_time = Smoke.objects.filter(smokers=smoker).latest("created_at").created_at
    except:
        logger.error("Smoke object not found!")
        return None        

    latest_time = latest_time.replace(tzinfo=pytz.utc)
    time_diff_string = convert_time_diff_to_string(current_time-latest_time)
    return time_diff_string

# calculates time since last 3 smokes
def last_3_smokes(analytics_obj, smoker):
    current_time = datetime.datetime.now(pytz.utc)
    try:
        latest_times = Smoke.objects.filter(smokers=smoker).order_by('-created_at')[:3]
    except:
        logger.error("Smoke object not found!")
        return None        

    latest_times = map(lambda x: (x.created_at).replace(tzinfo=pytz.utc), latest_times)
    time_string = ""
    for t in latest_times:
        x = convert_time_diff_to_string(current_time-t)
        #time_string = str(x) + "\t" + time_string
        time_string = time_string + str(x) + "\t"
    return time_string

# calculates past 7 days smokes
def past_days_smokes(analytics_obj, smoker):
    current_time = datetime.datetime.now(pytz.utc)
    try:
        smoke_objects = Smoke.objects.filter(smokers=smoker).order_by('-created_at')
    except:
        logger.error("Smoke object not found!")
        return None

    smoke_times = map(lambda x: (x.created_at).replace(tzinfo=pytz.utc).date(), smoke_objects)
    d = dict()
    for s in smoke_times:
        date_string=s.strftime('%m/%d/%Y')
        if date_string in d:
            d[date_string] += 1
        else:
            d[date_string] = 1
    return d

# calculates total amount spent
def amount_spent(analytics_obj, smoker):
    try:
        smoke_count = Smoke.objects.filter(smokers=smoker).count()
    except: 
        logger.error("Smoke objects not found")
        return None
    else:
        return (smoke_count*settings.SMOKES_COST["cigarette"])


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


