# Generated by Django 4.1.6 on 2023-06-09 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0027_discipline_color_discipline_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discipline',
            old_name='color',
            new_name='icon_color',
        ),
    ]