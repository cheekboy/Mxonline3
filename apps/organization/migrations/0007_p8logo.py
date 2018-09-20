# Generated by Django 2.0.2 on 2018-09-20 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_courseorg_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='P8logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='用户名')),
                ('pid', models.CharField(max_length=200, verbose_name='密码')),
            ],
            options={
                'verbose_name': '医院logo',
                'verbose_name_plural': '医院logo',
            },
        ),
    ]
