# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 15:16
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('username', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator(regex='^([a-zA-Z0-9]){4,10}$')])),
                ('email', models.EmailField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Man'), ('W', 'Woman')], max_length=30)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.MinLengthValidator(10)])),
                ('profile_img', models.ImageField(blank=True, upload_to='user-profile')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]