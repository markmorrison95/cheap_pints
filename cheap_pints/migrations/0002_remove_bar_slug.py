# Generated by Django 2.1.5 on 2020-06-03 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheap_pints', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bar',
            name='slug',
        ),
    ]
