# Generated by Django 3.1.1 on 2020-10-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0005_auto_20200930_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher',
            name='request_limit',
            field=models.IntegerField(default=0),
        ),
    ]
