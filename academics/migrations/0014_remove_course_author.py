# Generated by Django 4.1.6 on 2023-05-31 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0013_remove_course_course_dates_course_course_dates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='author',
        ),
    ]
