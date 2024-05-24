# Generated by Django 4.2.13 on 2024-05-23 12:22

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eveuniverse", "0010_alter_eveindustryactivityduration_eve_type_and_more"),
        ("wizardskillfarm", "0004_farmingskills_skill_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="characterfarmingskill",
            name="skill_type",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="eveuniverse.evetype",
            ),
        ),
    ]
