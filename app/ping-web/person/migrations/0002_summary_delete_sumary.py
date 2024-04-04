# Generated by Django 4.2.2 on 2023-10-17 05:55

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Summary",
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
                    "title",
                    models.CharField(max_length=50, verbose_name="Summary title"),
                ),
                ("content", mdeditor.fields.MDTextField()),
            ],
        ),
        migrations.DeleteModel(
            name="Sumary",
        ),
    ]