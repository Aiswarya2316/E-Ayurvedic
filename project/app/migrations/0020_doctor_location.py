# Generated by Django 5.1.6 on 2025-03-26 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_booking_customer_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
