# Generated by Django 3.1.4 on 2020-12-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201215_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[(None, 'Choose your gender'), ('Investor', 'Investor'), ('Borrower', 'Borrower')], max_length=50),
        ),
    ]
