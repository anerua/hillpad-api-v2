# Generated by Django 4.1.6 on 2023-06-09 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0036_disciplinedraft_discipline_discipline_draft'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageDraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name of language')),
                ('iso_639_code', models.CharField(blank=True, max_length=2, verbose_name='ISO 639 two-letter abbreviation')),
                ('status', models.CharField(choices=[('PUBLISHED', 'PUBLISHED'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'), ('REVIEW', 'REVIEW'), ('SAVED', 'SAVED')], default='SAVED', max_length=16, verbose_name='Degree Type status')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_draft_languages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='language',
            name='language_draft',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_language', to='academics.languagedraft'),
            preserve_default=False,
        ),
    ]