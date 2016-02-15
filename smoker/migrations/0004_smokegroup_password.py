# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smoker.models


class Migration(migrations.Migration):

    dependencies = [
        ('smoker', '0003_auto_20160202_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='smokegroup',
            name='password',
            field=models.CharField(max_length=200, null=True, verbose_name=smoker.models.Smoker, blank=True),
        ),
    ]
