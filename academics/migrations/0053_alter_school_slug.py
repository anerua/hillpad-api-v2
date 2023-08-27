# Generated by Django 4.1.6 on 2023-08-27 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0052_alter_course_slug_alter_school_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Unique school slug (autogenerated)'),
        ),
    ]
