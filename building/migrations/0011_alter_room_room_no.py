# Generated by Django 4.2.2 on 2023-06-24 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0010_room_room_document_url_room_room_photo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_no',
            field=models.CharField(max_length=100),
        ),
    ]
