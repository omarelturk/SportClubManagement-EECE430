# Generated by Django 4.0.3 on 2022-04-19 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scms_app', '0003_basketball_ticket_football_ticket_delete_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Football_Bought_Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('football_bought_ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scms_app.football_ticket')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Football_Bought_Ticket',
                'verbose_name_plural': 'Football_Bought_Tickets',
            },
        ),
        migrations.CreateModel(
            name='Basketball_Bought_Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basketball_bought_ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scms_app.basketball_ticket')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Basketball_Bought_Ticket',
                'verbose_name_plural': 'Basketball_Bought_Tickets',
            },
        ),
    ]
