# Generated by Django 4.1.13 on 2024-01-29 09:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
    ]
