# Generated by Django 4.2 on 2023-04-29 12:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(default='media/Default_user.png', upload_to='images/')),
                ('house_number', models.CharField(max_length=20, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Building created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Building Updated date')),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='files/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('text', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Request created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Request Updated date')),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.CharField(max_length=10)),
                ('criteria', models.CharField(choices=[('Fully Furnished', 'Fully Furnished'), ('Semi Furnished', 'Semi Furnished'), ('Not Furnished', 'Not Furnished')], default='Fully Furnished', max_length=15)),
                ('appliences', models.CharField(blank=True, max_length=100)),
                ('rent_amount', models.CharField(max_length=10)),
                ('advance', models.CharField(blank=True, max_length=10, null=True)),
                ('room_type', models.CharField(choices=[('3BHK', '3BHK'), ('2BHK', '2BHK'), ('1BHK', '1BHK'), ('Studio', 'Studio'), ('House', 'House'), ('Appartment', 'Appartment'), ('Others', 'Others')], default='House', max_length=10)),
                ('rent_period_start', models.DateField(verbose_name='rent period start')),
                ('rent_period_end', models.DateField(verbose_name='rent period end')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Room created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Room Updated date')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('floor', models.CharField(blank=True, max_length=100, null=True)),
                ('max_capacity', models.CharField(blank=True, max_length=2, null=True)),
                ('bathroom_count', models.CharField(blank=True, max_length=2, null=True)),
                ('kitchen_count', models.CharField(blank=True, max_length=2, null=True)),
                ('is_parking_available', models.BooleanField(default=True)),
                ('additional_photo', models.ManyToManyField(blank=True, to='building.documents')),
                ('building', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='building.building')),
            ],
        ),
    ]
