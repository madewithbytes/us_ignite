# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-22 04:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User responsible for this Challenge.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='entryanswer',
            unique_together=set([('entry', 'question')]),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('challenge', 'application')]),
        ),
    ]
