# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 13:18
from __future__ import unicode_literals

from django.db import migrations
from ..models import Season as SEASON


def insert_seasons(apps, schema_editor):
    """
    Create the four Seasons initially.
    """
    Season = apps.get_model("activities", "Season")
    season_objects = (Season(*choice) for choice in SEASON.SEASON_CHOICES)
    db_alias = schema_editor.connection.alias
    Season.objects.using(db_alias).bulk_create(season_objects)


def delete_seasons(apps, schema_editor):
    """
    Reverse function for deleting the four seasons.
    """
    Season = apps.get_model("activities", "Season")
    db_alias = schema_editor.connection.alias
    season_objects = (Season.objects.using(db_alias).filter(name=choice[0])
                      for choice in SEASON.SEASON_CHOICES)
    for obj in season_objects:
        obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_seasons, delete_seasons),
    ]
