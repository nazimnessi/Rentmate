# Generated by Django 4.2 on 2023-04-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='photo',
            field=models.ImageField(default='Default_user.png', upload_to='images/'),
        ),
    ]
