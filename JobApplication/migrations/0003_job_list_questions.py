# Generated by Django 4.2.4 on 2023-09-09 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobApplication', '0002_remove_job_application_question1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_list',
            name='questions',
            field=models.JSONField(blank=True, null=True),
        ),
    ]