# Generated by Django 2.0.2 on 2018-09-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_xiangyingshijian_zhujijiankong'),
    ]

    operations = [
        migrations.AddField(
            model_name='alikey',
            name='password',
            field=models.CharField(default='', max_length=200, verbose_name='密码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alikey',
            name='username',
            field=models.CharField(default='', max_length=200, verbose_name='用户名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alikey',
            name='init_script',
            field=models.CharField(max_length=8000, verbose_name='初始化脚本'),
        ),
    ]
