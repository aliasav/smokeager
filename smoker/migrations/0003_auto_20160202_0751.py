# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smoker', '0002_auto_20160118_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='smokeanalytic',
            name='daily_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='smokeanalytic',
            name='monthly_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='smokeanalytic',
            name='weekly_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='smokeanalytic',
            name='smoke_group',
            field=models.OneToOneField(related_name='smoke_analytic_group', null=True, blank=True, to='smoker.SmokeGroup'),
        ),
        migrations.AlterField(
            model_name='smokeanalytic',
            name='smoker',
            field=models.OneToOneField(related_name='smoke_analytic_individual', null=True, blank=True, to='smoker.Smoker'),
        ),
    ]
