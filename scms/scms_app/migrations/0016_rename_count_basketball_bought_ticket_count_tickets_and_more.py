# Generated by Django 4.0.3 on 2022-04-25 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scms_app', '0015_basketball_bought_ticket_count_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basketball_bought_ticket',
            old_name='count',
            new_name='count_tickets',
        ),
        migrations.RenameField(
            model_name='football_bought_ticket',
            old_name='count',
            new_name='count_tickets',
        ),
    ]