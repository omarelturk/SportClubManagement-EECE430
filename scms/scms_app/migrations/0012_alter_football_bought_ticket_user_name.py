# Generated by Django 4.0.3 on 2022-04-25 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scms_app', '0011_football_bought_ticket_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='football_bought_ticket',
            name='user_name',
            field=models.CharField(max_length=100),
        ),
    ]
