# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-13 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='ServerSettingsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('value', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'server_settings',
            },
        ),
        migrations.CreateModel(
            name='UserItemModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapp.ItemsModel')),
            ],
            options={
                'db_table': 'user_item',
            },
        ),
        migrations.CreateModel(
            name='UsersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=1024)),
                ('credit', models.FloatField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='useritemmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapp.UsersModel'),
        ),
        migrations.AlterUniqueTogether(
            name='useritemmodel',
            unique_together=set([('user', 'item')]),
        ),
    ]
