# Generated by Django 4.1.6 on 2023-06-02 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0015_alter_course_course_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_dates',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
