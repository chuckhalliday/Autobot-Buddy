# Generated by Django 4.1.13 on 2024-02-04 23:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_vehicle_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="name",
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
