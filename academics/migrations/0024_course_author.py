# Generated by Django 4.1.6 on 2023-06-08 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0023_language_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
