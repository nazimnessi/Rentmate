# Generated by Django 4.2.5 on 2023-09-24 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('building', '0014_alter_building_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='renter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='renter', to=settings.AUTH_USER_MODEL),
        ),
    ]