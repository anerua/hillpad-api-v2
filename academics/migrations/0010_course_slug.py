# Generated by Django 4.1.6 on 2023-04-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0009_alter_country_continent'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='Unique course slug (autogenerated)'),
        ),
    ]