# Generated by Django 2.2.3 on 2019-07-22 22:42

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200, unique=True)),
                ('expiration_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'db_table': 'token',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MS_Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_fsm.FSMField(choices=[('new', 'New'), ('started', 'Started'), ('paused', 'Paused'), ('win', 'Win'), ('lose', 'Lose')], db_index=True, default='new', max_length=50)),
                ('size', models.PositiveSmallIntegerField()),
                ('mines', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), size=None)),
                ('board', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('started', models.DateTimeField(null=True)),
                ('ended', models.DateTimeField(null=True)),
                ('ellapsed_time', models.TimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
                'db_table': 'game',
                'managed': True,
            },
        ),
    ]
