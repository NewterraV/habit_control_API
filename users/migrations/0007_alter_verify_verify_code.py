# Generated by Django 4.2.6 on 2023-10-10 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_verify_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verify',
            name='verify_code',
            field=models.PositiveIntegerField(default=70852, verbose_name='verify code'),
        ),
    ]
