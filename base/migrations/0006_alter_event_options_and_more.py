# Generated by Django 5.0.6 on 2024-06-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_alter_feedback_options_feedback_comment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={"ordering": ["date", "-location_name"]},
        ),
        migrations.RenameField(
            model_name="event",
            old_name="location",
            new_name="location_address",
        ),
        migrations.AddField(
            model_name="event",
            name="location_name",
            field=models.CharField(max_length=120, null=True),
        ),
    ]
