# Generated by Django 4.1.7 on 2023-04-01 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='alt_phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='media/Default_user.png', upload_to='images/'),
        ),
    ]
