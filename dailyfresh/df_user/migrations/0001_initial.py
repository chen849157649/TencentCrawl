# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('recipient_name', models.CharField(max_length=24, verbose_name='收件人')),
                ('recipient_addr', models.CharField(max_length=128, verbose_name='收件地址')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='电话')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮编')),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('username', models.CharField(max_length=20, verbose_name='账户')),
                ('password', models.CharField(max_length=40, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('is_active', models.BooleanField(verbose_name='激活状态', default=False)),
            ],
            options={
                'db_table': 'user_account',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='passport',
            field=models.ForeignKey(to='df_user.Passport'),
        ),
    ]
