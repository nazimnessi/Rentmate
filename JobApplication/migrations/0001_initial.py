# Generated by Django 4.2.3 on 2023-08-31 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('small_description', models.CharField(max_length=1000)),
                ('characteristics', models.JSONField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='job created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='job Updated date')),
            ],
        ),
        migrations.CreateModel(
            name='Job_Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('linkedIn', models.CharField(blank=True, max_length=300, null=True, unique=True)),
                ('github', models.CharField(blank=True, max_length=300, null=True, unique=True)),
                ('website', models.CharField(blank=True, max_length=300, null=True, unique=True)),
                ('total_experience', models.IntegerField()),
                ('question1', models.TextField(help_text='How did you hear about this position?:', max_length=1000)),
                ('question2', models.TextField(help_text='Why are you interested in joining the Rentmate team?:', max_length=1000)),
                ('question3', models.TextField(blank=True, help_text="ny additional information you'd like to share:", max_length=1000, null=True)),
                ('resume', models.CharField(max_length=200)),
                ('cover_letter', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='job created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='job Updated date')),
                ('Job_List', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Job_list', to='JobApplication.job_list')),
            ],
        ),
    ]
