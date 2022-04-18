# Generated by Django 4.0.3 on 2022-04-17 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basketball_Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=100)),
                ('player_number', models.IntegerField()),
                ('player_position', models.CharField(choices=[('Forward', 'Forward'), ('Center', 'Center'), ('Guard', 'Guard')], max_length=100)),
                ('player_nationality', models.CharField(max_length=100)),
                ('player_image', models.ImageField(upload_to='static/scms_app/images')),
            ],
            options={
                'verbose_name': 'Basketball_Player',
                'verbose_name_plural': 'Basketball_Players',
            },
        ),
        migrations.CreateModel(
            name='Football_Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=100)),
                ('player_number', models.IntegerField()),
                ('player_position', models.CharField(choices=[('Forward', 'Forward'), ('Midfielder', 'Midfielder'), ('Defender', 'Defender'), ('Goalkeeper', 'Goalkeeper')], max_length=100)),
                ('player_nationality', models.CharField(max_length=100)),
                ('player_image', models.ImageField(upload_to='static/scms_app/images')),
            ],
            options={
                'verbose_name': 'Football_Player',
                'verbose_name_plural': 'Football_Players',
            },
        ),
    ]