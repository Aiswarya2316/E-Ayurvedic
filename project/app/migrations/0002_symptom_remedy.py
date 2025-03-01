# Generated by Django 5.1.6 on 2025-02-24 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Remedy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('herbal_medicine', models.TextField()),
                ('dietary_plan', models.TextField()),
                ('yoga_practice', models.TextField()),
                ('lifestyle_adjustment', models.TextField()),
                ('symptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.symptom')),
            ],
        ),
    ]
