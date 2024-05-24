# Generated by Django 4.2.13 on 2024-05-24 08:42

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eveonline", "0017_alliance_and_corp_names_are_not_unique"),
        ("wizardskillfarm", "0005_alter_characterfarmingskill_skill_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounttimes",
            name="character",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="eveonline.evecharacter",
            ),
        ),
    ]
