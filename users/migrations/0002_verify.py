# Generated by Django 4.2.6 on 2023-10-05 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.PositiveIntegerField(blank=True, max_length=5, null=True, verbose_name='user code')),
                ('verify_code', models.PositiveIntegerField(default=99026, verbose_name='verify code')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verify', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
