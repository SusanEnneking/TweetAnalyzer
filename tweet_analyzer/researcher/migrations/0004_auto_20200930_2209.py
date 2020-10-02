# Generated by Django 3.1.1 on 2020-09-30 22:09

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0003_researcher_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researcher',
            name='time_zone',
            field=timezone_field.fields.TimeZoneField(default='America/Chicago', max_length=100),
        ),
    ]