from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from smoker import views as api_views

urlpatterns = [
    url(r'^signup$', api_views.signup),
    url(r'^increment_smoke$', api_views.increment_smoke),
    url(r'^get_stats$', api_views.get_stats),
]