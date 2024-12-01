# Generated by Django 5.1.1 on 2024-11-29 08:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('usertype', models.IntegerField(default=0)),
                ('password', models.CharField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('submission_num', models.IntegerField(default=10)),
                ('last_submission', models.DateTimeField(null=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.CharField(choices=[('en', 'english'), ('pl', 'polish')], max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_taken', models.FloatField(default=0)),
                ('llm_model', models.CharField(choices=[('bert-base', 'BERT Base'), ('bert-large', 'BERT Large'), ('roberta-base', 'Roberta Base'), ('roberta-large', 'Roberta Large')], max_length=20)),
                ('file', models.FileField(blank=True, null=True, upload_to='submission_files/')),
                ('entry', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
    ]
