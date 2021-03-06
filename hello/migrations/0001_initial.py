# Generated by Django 3.2.9 on 2021-12-04 00:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AidRequest',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('what_is_needed', models.CharField(max_length=1000)),
                ('completed', models.BooleanField(default=False)),
                ('zip_code', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('who_is_it_for_freeform_text',
                 models.CharField(max_length=100, null=True)),
                ('who_recorded_it_username', models.CharField(
                    max_length=100, null=True)),
            ],
        ),
    ]
