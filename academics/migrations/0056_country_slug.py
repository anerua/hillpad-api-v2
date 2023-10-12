# Generated by Django 4.1.6 on 2023-08-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0055_alter_discipline_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='Unique country slug (autogenerated)'),
        ),
    ]