# Generated by Django 4.2.6 on 2023-10-23 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("building", "0005_alter_building_building_photo_url_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="building",
            old_name="building_document_Url",
            new_name="building_document_url",
        ),
        migrations.RenameField(
            model_name="room",
            old_name="room_document_Url",
            new_name="room_document_url",
        ),
        migrations.RenameField(
            model_name="room",
            old_name="room_photo_Url",
            new_name="room_photo_url",
        ),
        migrations.AlterField(
            model_name="room",
            name="rent_period_end",
            field=models.DateField(
                blank=True,
                help_text="Rent period contract end date",
                null=True,
                verbose_name="rent period end",
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="rent_period_start",
            field=models.DateField(
                blank=True,
                help_text="Rent period contract start date",
                null=True,
                verbose_name="rent period start",
            ),
        ),
    ]
