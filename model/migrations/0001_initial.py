# Generated by Django 4.2.4 on 2023-08-03 18:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255, unique=True)),
                ('user_auth', models.CharField(max_length=255)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_on')),
            ],
        ),
    ]
