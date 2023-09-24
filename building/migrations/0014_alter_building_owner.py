# Generated by Django 4.2.5 on 2023-09-24 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('building', '0013_alter_room_room_photo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='building', to=settings.AUTH_USER_MODEL),
        ),
    ]