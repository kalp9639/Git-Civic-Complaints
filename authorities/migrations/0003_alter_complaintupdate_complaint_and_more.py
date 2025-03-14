# Generated by Django 5.1.6 on 2025-03-05 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorities", "0002_officialprofile"),
        ("complaints", "0002_complaint_latitude_complaint_longitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="complaintupdate",
            name="complaint",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authority_updates",
                to="complaints.complaint",
            ),
        ),
        migrations.AlterField(
            model_name="complaintupdate",
            name="official",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authority_complaint_updates",
                to="authorities.governmentofficial",
            ),
        ),
        migrations.DeleteModel(
            name="OfficialProfile",
        ),
    ]
