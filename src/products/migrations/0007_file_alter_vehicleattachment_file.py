# Generated by Django 4.1.13 on 2024-02-04 23:01

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_alter_vehicleattachment_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        storage=django.core.files.storage.FileSystemStorage(
                            location="/Users/charlesclark/Desktop/codingProjects/AutoAdvisor/local-cdn/protected"
                        ),
                        upload_to=products.models.handle_vehicle_attachment_upload,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="vehicleattachment",
            name="file",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="products.file"
            ),
        ),
    ]