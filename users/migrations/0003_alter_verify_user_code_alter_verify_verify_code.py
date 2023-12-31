# Generated by Django 4.2.6 on 2023-10-06 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verify',
            name='user_code',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='user code'),
        ),
        migrations.AlterField(
            model_name='verify',
            name='verify_code',
            field=models.PositiveIntegerField(default=25741, verbose_name='verify code'),
        ),
    ]
