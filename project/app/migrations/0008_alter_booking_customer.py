# Generated by Django 5.1.6 on 2025-02-26 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_booking_status_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='app.customer'),
        ),
    ]
