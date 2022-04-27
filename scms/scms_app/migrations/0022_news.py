# Generated by Django 4.0.3 on 2022-04-27 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scms_app', '0021_alter_merchandise_bought_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_header', models.CharField(max_length=200)),
                ('news_image', models.ImageField(upload_to='')),
                ('news_text', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
    ]
