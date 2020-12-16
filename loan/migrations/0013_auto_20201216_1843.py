# Generated by Django 3.1.4 on 2020-12-16 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0012_auto_20201216_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='paid_monthes',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='start_date',
        ),
        migrations.AddField(
            model_name='offer',
            name='paid_monthes',
            field=models.IntegerField(default=0),
        ),
    ]