# Generated by Django 5.0.1 on 2024-01-09 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CentralizedHospitalApp', '0004_remove_appointment_doctorid'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='hname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
