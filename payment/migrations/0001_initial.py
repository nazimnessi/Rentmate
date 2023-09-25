# Generated by Django 4.2.5 on 2023-09-25 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('building', '0015_alter_room_renter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Unpaid', 'Unpaid')], max_length=20, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=80, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Payment date')),
                ('payee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments_received', to=settings.AUTH_USER_MODEL)),
                ('payer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments_done', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='building.room')),
            ],
        ),
    ]
