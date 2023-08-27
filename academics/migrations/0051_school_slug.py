# Generated by Django 4.1.6 on 2023-08-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0050_alter_countrydraft_options_alter_course_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Unique school slug (autogenerated)'),
        ),
    ]