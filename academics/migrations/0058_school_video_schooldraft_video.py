# Generated by Django 4.1.6 on 2023-10-15 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0057_alter_currency_usd_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='video',
            field=models.URLField(blank=True, verbose_name='School Youtube video'),
        ),
        migrations.AddField(
            model_name='schooldraft',
            name='video',
            field=models.URLField(blank=True, verbose_name='School Youtube video'),
        ),
    ]