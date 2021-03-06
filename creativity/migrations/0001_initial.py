# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-25 10:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('published_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Creativity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motive', models.CharField(choices=[('player', 'Player'), ('feature', 'Feature')], default='player', max_length=7)),
                ('name', models.CharField(max_length=75)),
                ('desc', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=6)),
                ('views', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creativities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Likeability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(0, 'NOVOTE'), (1, 'UPVOTE')], default=0)),
                ('creativity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creati_vote_levels', to='creativity.Creativity')),
            ],
        ),
        migrations.CreateModel(
            name='UpVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_vote', models.IntegerField(null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='likeability',
            name='users_vote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creati_vote_levels', to='creativity.UpVote'),
        ),
        migrations.AddField(
            model_name='creativity',
            name='upvotes',
            field=models.ManyToManyField(related_name='creativities', through='creativity.Likeability', to='creativity.UpVote'),
        ),
        migrations.AddField(
            model_name='comment',
            name='creativity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creati_comments', to='creativity.Creativity'),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creati_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='likeability',
            unique_together=set([('creativity', 'users_vote')]),
        ),
    ]
