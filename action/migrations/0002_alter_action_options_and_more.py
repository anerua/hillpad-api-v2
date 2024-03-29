# Generated by Django 4.1.6 on 2023-06-06 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveIndex(
            model_name='action',
            name='action_acti_content_59b007_idx',
        ),
        migrations.RenameField(
            model_name='action',
            old_name='object_id',
            new_name='entry_object_id',
        ),
        migrations.RemoveField(
            model_name='action',
            name='content_type',
        ),
        migrations.AddField(
            model_name='action',
            name='entry_object_type',
            field=models.CharField(choices=[('country', 'Country'), ('course', 'Course'), ('currency', 'Currency'), ('degree_type', 'Degree Type'), ('discipline', 'Discipline'), ('language', 'Language'), ('programme_type', 'Programme Type'), ('school', 'School')], default='course', max_length=16, verbose_name='Entry object type'),
            preserve_default=False,
        ),
    ]
