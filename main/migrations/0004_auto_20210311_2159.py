# Generated by Django 3.0.5 on 2021-03-11 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210311_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки'},
        ),
    ]
