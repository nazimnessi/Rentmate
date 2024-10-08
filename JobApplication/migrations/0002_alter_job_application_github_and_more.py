# Generated by Django 4.2.6 on 2023-10-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("JobApplication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job_application",
            name="github",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="job_application",
            name="linkedIn",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="job_application",
            name="website",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
