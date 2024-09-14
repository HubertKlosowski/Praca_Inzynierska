# Generated by Django 5.1 on 2024-09-14 17:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_created_at_alter_user_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('llm_model', models.CharField(choices=[('bert-base', 'BERT Base'), ('bert-large', 'BERT Large')], max_length=20)),
                ('file', models.FileField(upload_to='files/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
    ]
