# Generated by Django 4.1.13 on 2024-02-04 21:04

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_remove_vehicle_image_vehicle_timestamp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicleattachment",
            name="file",
            field=models.FileField(
                storage=django.core.files.storage.FileSystemStorage(
                    location="/Users/charlesclark/Desktop/codingProjects/AutoAdvisor/local-cdn/protected"
                ),
                upload_to=products.models.handle_vehicle_attachment_upload,
            ),
        ),
    ]