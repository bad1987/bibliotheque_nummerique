# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-06 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('numerique', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logiciel',
            name='categorie',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
