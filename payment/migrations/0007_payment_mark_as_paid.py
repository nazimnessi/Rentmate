# Generated by Django 4.2.6 on 2023-11-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_payment_bill_image_url_payment_is_expense"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="mark_as_paid",
            field=models.BooleanField(default=False),
        ),
    ]
