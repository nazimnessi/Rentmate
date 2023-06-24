# Generated by Django 4.2 on 2023-05-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country_code',
            field=models.CharField(choices=[('code_1', 'United States'), ('code_91', 'India'), ('code_86', 'China'), ('code_44', 'United Kingdom'), ('code_49', 'Germany'), ('code_966', 'Saudi Arabia')], db_column='building_type', default='India', max_length=10),
        ),
    ]