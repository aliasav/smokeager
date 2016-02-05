# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Smoke',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmokeAnalytic',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, db_index=True)),
                ('daily_target', models.IntegerField(default=0, null=True, blank=True)),
                ('smoke_count', models.IntegerField(default=0, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmokeGroup',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, db_index=True)),
                ('name', models.CharField(max_length=300, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Smoker',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, db_index=True)),
                ('name', models.CharField(max_length=300, null=True, blank=True)),
                ('email', models.CharField(max_length=300, null=True, db_index=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(related_name='smoker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='smokegroup',
            name='admin',
            field=models.OneToOneField(related_name='group_admin', null=True, blank=True, to='smoker.Smoker'),
        ),
        migrations.AddField(
            model_name='smokegroup',
            name='smokers',
            field=models.ManyToManyField(related_name='smoke_group', null=True, to='smoker.Smoker', blank=True),
        ),
        migrations.AddField(
            model_name='smokeanalytic',
            name='smoke_group',
            field=models.OneToOneField(related_name='smoke_group', null=True, blank=True, to='smoker.SmokeGroup'),
        ),
        migrations.AddField(
            model_name='smokeanalytic',
            name='smoker',
            field=models.OneToOneField(related_name='smoker_individual', null=True, blank=True, to='smoker.Smoker'),
        ),
        migrations.AddField(
            model_name='smoke',
            name='smokers',
            field=models.ManyToManyField(related_name='smokers', null=True, to='smoker.Smoker', blank=True),
        ),
    ]
