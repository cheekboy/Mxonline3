# Generated by Django 2.0.2 on 2018-09-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_alifee_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AliLaXin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shouGou', models.CharField(max_length=200, verbose_name='首购时间')),
                ('shengFen', models.CharField(max_length=200, verbose_name='省份')),
                ('daiLi', models.CharField(max_length=200, verbose_name='代理')),
                ('WangDian', models.CharField(max_length=200, verbose_name='网点名称')),
                ('kehuJingli', models.CharField(max_length=200, verbose_name='客户经理')),
                ('mob', models.CharField(max_length=200, verbose_name='用户手机号')),
                ('reg', models.CharField(max_length=200, verbose_name='注册时间')),
                ('status', models.CharField(max_length=200, verbose_name='用户状态')),
                ('bangka', models.CharField(max_length=200, verbose_name='是否绑卡')),
                ('orderId', models.CharField(max_length=200, verbose_name='首购订单')),
            ],
            options={
                'verbose_name': '阿里拉新',
                'verbose_name_plural': '阿里拉新',
            },
        ),
        migrations.AlterModelOptions(
            name='alifee',
            options={'verbose_name': '余额', 'verbose_name_plural': '余额'},
        ),
    ]
