# Generated by Django 5.1.6 on 2025-02-26 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_booking_customer_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
