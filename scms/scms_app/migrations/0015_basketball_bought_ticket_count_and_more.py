# Generated by Django 4.0.3 on 2022-04-25 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scms_app', '0014_alter_basketball_bought_ticket_user_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketball_bought_ticket',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='football_bought_ticket',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
