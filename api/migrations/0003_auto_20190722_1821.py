# Generated by Django 2.1.7 on 2019-07-22 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190722_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruleinfo',
            name='desc',
            field=models.CharField(max_length=200, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='ruleinfo',
            name='proxy',
            field=models.CharField(max_length=20, null=True, verbose_name='转发代理'),
        ),
        migrations.AlterField(
            model_name='ruleinfo',
            name='request_body',
            field=models.TextField(null=True, verbose_name='请求'),
        ),
    ]