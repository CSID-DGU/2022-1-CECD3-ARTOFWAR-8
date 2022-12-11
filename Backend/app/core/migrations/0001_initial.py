# Generated by Django 3.1 on 2022-08-22 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('ID', models.CharField(max_length=45)),
                ('name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=100)),
                ('uid', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'userInfo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Videoinfo',
            fields=[
                ('vid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('mjclass', models.CharField(blank=True, max_length=45, null=True)),
                ('subclass', models.CharField(blank=True, max_length=45, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('introduction', models.CharField(blank=True, max_length=45, null=True)),
                ('storage_key', models.CharField(blank=True, max_length=45, null=True)),
                ('storage_url', models.CharField(blank=True, max_length=45, null=True)),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.DO_NOTHING, to='core.userinfo')),
            ],
            options={
                'db_table': 'videoInfo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Inquire',
            fields=[
                ('qid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=300, null=True)),
                ('question', models.CharField(blank=True, max_length=300, null=True)),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.DO_NOTHING, to='core.userinfo')),
                ('vid', models.ForeignKey(db_column='vid', on_delete=django.db.models.deletion.DO_NOTHING, to='core.videoinfo')),
            ],
            options={
                'db_table': 'inquire',
                'managed': True,
            },
        ),
    ]