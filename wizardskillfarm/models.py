"""
App Models
Create your models in here
"""

# Third Party

# Django
from django.contrib.auth.models import User
from django.db import models

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth (External Libs)
from eveuniverse.models import EveType


class AccountTimes(models.Model):
    character = models.OneToOneField(
        EveCharacter, on_delete=models.CASCADE, null=False, default=None
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounttimes", unique=False
    )
    expiry = models.DateTimeField(null=False, default=None, blank=False)
    type = models.CharField(max_length=200)


class FarmingSkills(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="farmingskills", unique=False
    )
    skill_id = models.IntegerField()
    skill_type = models.ForeignKey(
        EveType, on_delete=models.CASCADE, related_name="farmingskills", unique=False
    )


class ExcludedCharacterFarmingSkills(models.Model):
    character = models.ForeignKey(
        EveCharacter, on_delete=models.CASCADE, null=False, default=None
    )
    skill_id = models.IntegerField()


class FarmingCharacters(models.Model):
    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="farmingcharacters", unique=False
    )

    active = models.BooleanField(default=True)

    last_update = models.DateTimeField(null=True, default=None, blank=True)

    total_large_extractors = models.IntegerField()

    excluded_skills = models.ForeignKey(
        ExcludedCharacterFarmingSkills, on_delete=models.CASCADE, null=True
    )


class CharacterFarmingSkill(models.Model):
    character = models.ForeignKey(
        EveCharacter, on_delete=models.CASCADE, null=False, default=None
    )
    skill_type = models.ForeignKey(
        EveType, on_delete=models.DO_NOTHING, unique=False, null=True, default=None
    )
    skill_level = models.IntegerField()
    sp_in_skill = models.IntegerField()

    farming_character = models.ForeignKey(
        FarmingCharacters,
        on_delete=models.CASCADE,
        null=True,
        related_name="farming_skills",
    )


class DustyBotSkillQueueCheck(models.Model):
    character = models.OneToOneField(
        EveCharacter, on_delete=models.CASCADE, null=False, default=None
    )
    last_alerted = models.DateTimeField(null=False, default=None, blank=False)


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)
