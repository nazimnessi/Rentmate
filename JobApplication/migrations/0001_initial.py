# Generated by Django 4.2.6 on 2023-10-14 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Job_Types",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="job type created date"
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="job type Updated date"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Job_List",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("small_description", models.CharField(max_length=1000)),
                ("characteristics", models.JSONField(max_length=100)),
                ("questions", models.JSONField(blank=True, null=True)),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="job created date"
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="job Updated date"
                    ),
                ),
                (
                    "jobTypes",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Job_type",
                        to="JobApplication.job_types",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Job_Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=50, unique=True)),
                ("phone_number", models.CharField(max_length=100, unique=True)),
                (
                    "linkedIn",
                    models.CharField(
                        blank=True, max_length=300, null=True, unique=True
                    ),
                ),
                (
                    "github",
                    models.CharField(
                        blank=True, max_length=300, null=True, unique=True
                    ),
                ),
                (
                    "website",
                    models.CharField(
                        blank=True, max_length=300, null=True, unique=True
                    ),
                ),
                ("total_experience", models.IntegerField()),
                ("questions", models.JSONField(blank=True, null=True)),
                ("resume", models.CharField(max_length=200)),
                (
                    "cover_letter",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("photo", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="job created date"
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="job Updated date"
                    ),
                ),
                (
                    "Job_List",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="Job_list",
                        to="JobApplication.job_list",
                    ),
                ),
            ],
        ),
    ]
