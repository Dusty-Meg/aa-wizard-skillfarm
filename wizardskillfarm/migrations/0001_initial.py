# Generated by Django 4.0.10 on 2023-09-07 15:12

# Django
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("eveonline", "0017_alliance_and_corp_names_are_not_unique"),
        ("corptools", "0086_characterindustryjob"),
    ]

    operations = [
        migrations.CreateModel(
            name="General",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "permissions": (("basic_access", "Can access this app"),),
                "managed": False,
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="ExcludedCharacterFarmingSkills",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("skill_id", models.IntegerField()),
                (
                    "character",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveonline.evecharacter",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FarmingSkills",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("skill_id", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FarmingCharacters",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "last_update",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("total_large_extractors", models.IntegerField()),
                (
                    "character",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveonline.evecharacter",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        default=None,
                        null=True,
                    ),
                ),
                (
                    "excluded_skills",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wizardskillfarm.excludedcharacterfarmingskills",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CharacterFarmingSkill",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("skill_level", models.IntegerField()),
                ("sp_in_skill", models.IntegerField()),
                (
                    "character",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveonline.evecharacter",
                    ),
                ),
                (
                    "skill_type",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="corptools.eveitemtype",
                    ),
                ),
                (
                    "farming_character",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wizardskillfarm.farmingcharacters",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccountTimes",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "expiry",
                    models.DateTimeField(blank=False, default=None, null=False),
                ),
                (
                    "character",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveonline.evecharacter",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        default=None,
                        null=True,
                    ),
                ),
                ("type", models.CharField(max_length=200)),
            ],
        ),
    ]