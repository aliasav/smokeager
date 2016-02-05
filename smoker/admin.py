from django.contrib import admin
from smoker.models import Smoker, SmokeGroup, Smoke, SmokeAnalytic


class SmokerAdmin(admin.ModelAdmin):

    list_display = ('guid', 'name', 'phone', 'email', 'created_at', 'updated_at')

    search_fields = ['guid', 'name', 'phone', 'email']

admin.site.register(Smoker, SmokerAdmin)



class SmokeGroupAdmin(admin.ModelAdmin):

    list_display = ('guid', 'name', 'admin', 'get_smokers', 'created_at', 'updated_at')

    search_fields = ['guid', 'name', 'admin']

admin.site.register(SmokeGroup, SmokeGroupAdmin)



class SmokeAdmin(admin.ModelAdmin):

    list_display = ('guid', 'created_at', 'updated_at')

    search_fields = ['guid']

admin.site.register(Smoke, SmokeAdmin)



class SmokeAnalyticAdmin(admin.ModelAdmin):

    list_display = ('guid', 'smoker', 'smoke_group', 'daily_count', 'weekly_count', 'monthly_count', \
    				'smoke_count', 'daily_target', 'created_at', 'updated_at')

    search_fields = ['guid']

admin.site.register(SmokeAnalytic, SmokeAnalyticAdmin)
