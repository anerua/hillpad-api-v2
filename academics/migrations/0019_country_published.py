# Generated by Django 4.1.6 on 2023-06-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0018_school_published_school_reject_reason_school_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Published status of course'),
        ),
    ]
