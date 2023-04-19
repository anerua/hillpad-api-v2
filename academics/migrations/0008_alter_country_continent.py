# Generated by Django 4.1.6 on 2023-04-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0007_alter_country_continent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='continent',
            field=models.CharField(choices=[('AF', 'Africa'), ('AS', 'Asia'), ('EU', 'Europe'), ('NA', 'North America'), ('SA', 'South America'), ('OC', 'Oceania'), ('AN', 'Antarctica')], max_length=16, verbose_name='Continent'),
        ),
    ]
