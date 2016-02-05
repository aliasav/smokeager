# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smoker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smoke',
            name='smokers',
            field=models.ManyToManyField(related_name='smokers', to='smoker.Smoker', blank=True),
        ),
        migrations.AlterField(
            model_name='smokegroup',
            name='smokers',
            field=models.ManyToManyField(related_name='smoke_group', to='smoker.Smoker', blank=True),
        ),
    ]
