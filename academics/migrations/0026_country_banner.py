# Generated by Django 4.1.6 on 2023-06-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0025_school_banner_school_city_school_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/academics/country/banners'),
        ),
    ]
