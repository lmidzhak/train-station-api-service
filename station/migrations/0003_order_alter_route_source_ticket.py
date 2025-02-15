# Generated by Django 4.0.4 on 2024-08-20 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('station', '0002_crewmember_route_journey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='route',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_sources', to='station.station'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo_number', models.IntegerField()),
                ('seat_number', models.IntegerField()),
                ('journey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='station.journey')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='station.order')),
            ],
            options={
                'ordering': ['cargo_number', 'seat_number'],
                'unique_together': {('journey', 'cargo_number', 'seat_number')},
            },
        ),
    ]
