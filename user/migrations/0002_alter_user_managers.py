# Generated by Django 4.0.4 on 2024-08-26 11:46

from django.db import migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
    ]
