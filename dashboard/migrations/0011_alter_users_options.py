# Generated by Django 4.2.5 on 2024-04-17 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Subscription', 'verbose_name_plural': 'Subscription Types'},
        ),
    ]