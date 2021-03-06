# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-20 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influence', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likeability',
            old_name='vote',
            new_name='users_vote',
        ),
        migrations.RemoveField(
            model_name='upvote',
            name='users_votes',
        ),
        migrations.AddField(
            model_name='upvote',
            name='users_vote',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='likeability',
            unique_together=set([('influence', 'users_vote')]),
        ),
    ]
