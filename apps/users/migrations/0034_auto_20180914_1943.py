# Generated by Django 2.0.1 on 2018-09-14 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20180914_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yunweizu',
            old_name='shouji_haoma',
            new_name='beizu',
        ),
        migrations.RemoveField(
            model_name='yunweizu',
            name='youxiang',
        ),
    ]
