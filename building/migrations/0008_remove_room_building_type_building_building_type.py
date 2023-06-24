# Generated by Django 4.2 on 2023-05-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0007_room_building_type_alter_room_room_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='building_type',
        ),
        migrations.AddField(
            model_name='building',
            name='building_type',
            field=models.CharField(choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Others', 'Others')], db_column='building_type', default='House', max_length=10),
        ),
    ]