"""
App Models
Create your models in here
"""

# Third Party
from corptools.models import EveItemType

# Django
from django.contrib.auth.models import User
from django.db import models

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter


class FarmingSkills(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, default=None
    )
    skill_id = models.IntegerField()


class ExcludedCharacterFarmingSkills(models.Model):
    character = models.ForeignKey(
        EveCharacter, on_delete=models.CASCADE, null=False, default=None
    )
    skill_id = models.IntegerField()


class CharacterFarmingSkill(models.Model):
    character = models.ForeignKey(
        EveCharacter, on_delete=models.CASCADE, null=False, default=None
    )
    skill_id = models.IntegerField()
    skill_name = models.ForeignKey(
        EveItemType, on_delete=models.CASCADE, null=True, default=None
    )


class FarmingCharacters(models.Model):
    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="farmingcharacters"
    )

    active = models.BooleanField(default=True)

    last_update = models.DateTimeField(null=True, default=None, blank=True)

    total_extract_sp = models.BigIntegerField()
    total_large_extractors = models.IntegerField()

    excluded_skills = models.ForeignKey(
        ExcludedCharacterFarmingSkills, on_delete=models.CASCADE, null=True
    )

    farming_skills = models.ForeignKey(
        CharacterFarmingSkill, on_delete=models.CASCADE, null=True
    )


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)
