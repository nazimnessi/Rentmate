# Generated by Django 4.1.7 on 2023-04-02 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_phone_number_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]