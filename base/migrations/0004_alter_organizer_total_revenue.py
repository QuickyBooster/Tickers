# Generated by Django 5.0.6 on 2024-06-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_organizer_legal_representative_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizer",
            name="total_revenue",
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
    ]
