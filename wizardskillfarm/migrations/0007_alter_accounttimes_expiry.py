# Generated by Django 4.2.13 on 2024-05-24 09:49

# Django
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wizardskillfarm", "0006_alter_accounttimes_character"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounttimes",
            name="expiry",
            field=models.DateTimeField(default=None),
        ),
    ]