from django.conf.urls import url
from django.conf.urls.static import static

from smoker import views as api_views

urlpatterns = [
    url(r'^signup$', api_views.signup),
    url(r'^increment_smoke$', api_views.increment_smoke),
    url(r'^get_stats$', api_views.get_stats),
]