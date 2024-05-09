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


class AccountTimes(models.Model):
    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounttimes"
    )
    expiry = models.DateField(null=False, default=None, blank=False)
    type = models.CharField(max_length=200)


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
        EveItemType,
        on_delete=models.DO_NOTHING,
        null=True,
        default=None,
    )
    skill_level = models.IntegerField()
    sp_in_skill = models.IntegerField()

    farming_character = models.ForeignKey(
        FarmingCharacters,
        on_delete=models.CASCADE,
        null=True,
        related_name="farming_skills",
    )


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)
