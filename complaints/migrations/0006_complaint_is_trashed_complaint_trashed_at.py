# Generated by Django 5.1.6 on 2025-03-19 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("complaints", "0005_delete_complaintupdate"),
    ]

    operations = [
        migrations.AddField(
            model_name="complaint",
            name="is_trashed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="complaint",
            name="trashed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
