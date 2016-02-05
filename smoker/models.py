from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime, uuid, logging
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


# smoker model for customer, extends django User model
class Smoker(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.OneToOneField(User, db_index=True, related_name="smoker")
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=False, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):

        return "%s<----->%s" %(self.guid, self.email)

# post save for creating smoker on User creation
def create_smoker(sender, instance, created, **kwargs):

    if created:
        smoker, created = Smoker.objects.get_or_create(user=instance, email=instance.email)

        # create user's token
        user = smoker.user
        token = Token.objects.create(user=user)
        logger.debug("Token created for user %s: %s" %(user, token))

        # create smoke analytic object for smoker
        smoke_analytic = SmokeAnalytic.objects.create(smoker=smoker)
        logger.debug("smoke analytic object creted for smoker: %s" %(smoke_analytic))

post_save.connect(create_smoker, sender=User)

# smoke group
class SmokeGroup(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    admin = models.OneToOneField(Smoker, related_name="group_admin", null=True, blank=True)
    password = models.CharField(Smoker, null=True, blank=True, max_length=200)

    smokers = models.ManyToManyField(Smoker, related_name="smoke_group", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_smokers(self, obj):
        return "\n".join([s.email for s in obj.smokers.all()])


    def __unicode__(self):

        return "%s<---->%s" %(self.guid, self.name)


# smoke object (cigarette/joint/cigar)!
# saved each time a smoker smokes
class Smoke(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)

    smokers = models.ManyToManyField(Smoker, related_name="smokers", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_smokers(self, obj):
        return "\n".join([s.email for s in obj.smokers.all()])

    def __unicode__(self):

        return "%s" %(self.guid)


# smoke analytics object
# each user will have a smoke analytics object associated with himself/herself
# each smoke group will have a smoke analytics object assoicated with itself
# will contain all information that analyses smoking habits of user/group
class SmokeAnalytic(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    
    smoker = models.OneToOneField(Smoker, related_name="smoke_analytic_individual", null=True, blank=True)
    smoke_group = models.OneToOneField(SmokeGroup, related_name="smoke_analytic_group", null=True, blank=True)

    daily_target = models.IntegerField(default=0, null=True, blank=True)
    smoke_count = models.IntegerField(default=0, null=True, blank=True)

    daily_count = models.IntegerField(default=0, null=True, blank=True)
    weekly_count = models.IntegerField(default=0, null=True, blank=True)
    monthly_count = models.IntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):

        return "%s<------>%s<------>%s" %(self.guid, self.smoker, self.smoke_group)

