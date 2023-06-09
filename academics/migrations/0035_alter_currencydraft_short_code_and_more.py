# Generated by Django 4.1.6 on 2023-06-09 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0034_currencydraft_currency_currency_draft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencydraft',
            name='short_code',
            field=models.CharField(blank=True, max_length=3, verbose_name='Short code of the currency (ISO 4217)'),
        ),
        migrations.AlterField(
            model_name='currencydraft',
            name='status',
            field=models.CharField(choices=[('PUBLISHED', 'PUBLISHED'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'), ('REVIEW', 'REVIEW'), ('SAVED', 'SAVED')], default='SAVED', max_length=16, verbose_name='Currency status'),
        ),
        migrations.AlterField(
            model_name='currencydraft',
            name='usd_exchange_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='Exchange rate with the USD'),
        ),
        migrations.CreateModel(
            name='DegreeTypeDraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name of degree type, e.g. Bachelor of Science')),
                ('short_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Short name of degree type, e.g. B.Sc.')),
                ('status', models.CharField(choices=[('PUBLISHED', 'PUBLISHED'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'), ('REVIEW', 'REVIEW'), ('SAVED', 'SAVED')], default='SAVED', max_length=16, verbose_name='Degree Type status')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_draft_degree_types', to=settings.AUTH_USER_MODEL)),
                ('programme_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme_type_draft_degree_types', to='academics.programmetype')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='degreetype',
            name='degree_type_draft',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_degree_type', to='academics.degreetypedraft'),
            preserve_default=False,
        ),
    ]
