# Generated by Django 3.1.4 on 2020-12-16 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan', '0007_auto_20201216_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='investor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='offer',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]