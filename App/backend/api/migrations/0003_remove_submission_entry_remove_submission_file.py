# Generated by Django 5.1 on 2024-11-24 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_submission_sent_at_submission_time_taken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='file',
        ),
    ]
