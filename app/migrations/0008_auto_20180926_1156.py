# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-26 11:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_goods'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='spcifics',
            new_name='specifics',
        ),
    ]
