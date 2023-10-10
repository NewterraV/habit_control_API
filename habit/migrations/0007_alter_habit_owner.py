# Generated by Django 4.2.6 on 2023-10-10 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habit', '0006_alter_habit_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='habit', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
