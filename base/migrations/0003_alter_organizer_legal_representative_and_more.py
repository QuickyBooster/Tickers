# Generated by Django 5.0.6 on 2024-06-04 07:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_alter_user_award_point_alter_user_dob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizer",
            name="legal_representative",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="organizer",
            name="tax_code",
            field=models.CharField(
                max_length=10,
                validators=[
                    django.core.validators.MinLengthValidator(
                        10, "This field must contain at least 10 chars"
                    )
                ],
            ),
        ),
    ]
