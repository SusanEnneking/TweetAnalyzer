# Generated by Django 3.1.1 on 2020-09-30 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='message',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='search',
            name='query',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='search',
            name='query_url',
            field=models.CharField(default='', max_length=1500),
        ),
        migrations.AlterField(
            model_name='search',
            name='twitter_response_status',
            field=models.CharField(default='', max_length=3),
        ),
    ]