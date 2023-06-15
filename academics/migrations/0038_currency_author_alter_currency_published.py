# Generated by Django 4.1.6 on 2023-06-15 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0037_languagedraft_language_language_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_currencies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='currency',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Published status of currency'),
        ),
    ]