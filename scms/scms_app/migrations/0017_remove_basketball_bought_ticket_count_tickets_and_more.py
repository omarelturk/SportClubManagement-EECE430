# Generated by Django 4.0.3 on 2022-04-25 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scms_app', '0016_rename_count_basketball_bought_ticket_count_tickets_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basketball_bought_ticket',
            name='count_tickets',
        ),
        migrations.RemoveField(
            model_name='football_bought_ticket',
            name='count_tickets',
        ),
    ]
