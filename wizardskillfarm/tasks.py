"""App Tasks"""

# Standard Library
import datetime
import logging

# Third Party
from celery import shared_task
from corptools.models import Skill, SkillQueue

# Django
from django.contrib.auth.models import User

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth (External Libs)
from eveuniverse.models import EveType

from .models import CharacterFarmingSkill, FarmingCharacters

logger = logging.getLogger(__name__)


@shared_task
def update_farming_characters():
    all_users = User.objects.all()

    for user in all_users:
        if len(user.farmingcharacters.all()) > 0:
            for character in user.farmingcharacters.all():
                update_farming_character.delay(character.character_id, user.id)


def getSpInSkill(activeLevel, skill):
    modifier, _ = EveType.objects.get_or_create_esi(
        id=skill.id, include_children=True, enabled_sections=[EveType.Section.DOGMAS]
    )
    modifier.save()

    type = modifier.dogma_attributes.get(eve_dogma_attribute_id=275)

    match activeLevel:
        case 1:
            return 256 * type.value
        case 2:
            return 1414 * type.value
        case 3:
            return 8000 * type.value
        case 4:
            return 45255 * type.value
        case 5:
            return 256000 * type.value
        case _:
            return 0


@shared_task
def update_farming_character_user(user_id: int):
    user = User.objects.filter(id=user_id).first()
    farming_characters = user.farmingcharacters.all()

    for character in farming_characters:
        update_farming_character.delay(character.character_id, user.id)


@shared_task
def update_farming_character(character_id: int, user_id: int):
    user = User.objects.filter(id=user_id).first()
    character = EveCharacter.objects.filter(character_id=character_id).first()
    character_skills = Skill.objects.filter(character_id=character_id)
    character_skillqueue = SkillQueue.objects.filter(character_id=character_id)
    farming_skills = user.farmingskills.all()
    farm_character = FarmingCharacters.objects.filter(character=character).first()

    char_farm_skills = CharacterFarmingSkill.objects.filter(character=character)

    total_sp = 0

    for skill in character_skillqueue:
        if skill.finish_date and skill.finish_date < datetime.datetime.now(
            datetime.timezone.utc
        ):
            character_skill = [
                c_k for c_k in character_skills if c_k.skill_id == skill.skill_id
            ]

            if not character_skill:
                character_skill[0].active_skill_level = skill.level_end
                character_skill[0].save()

    for skill in farming_skills:
        farming_skill = [
            c_f_s for c_f_s in char_farm_skills if c_f_s.skill_type_id == skill.skill_id
        ]

        if len(farming_skill) > 0:
            farming_skill = CharacterFarmingSkill()
        else:
            farming_skill = farming_skill[0]

        farming_skill.character = character
        farming_skill.skill_type = skill.skill_type
        farming_skill.farming_character = farm_character
        farming_skill.skill_level = 0
        farming_skill.sp_in_skill = 0

        char_skill = [c_k for c_k in character_skills if c_k.skill_id == skill.skill_id]

        if len(char_skill) > 0:
            farming_skill.skill_level = char_skill[0].active_skill_level
            farming_skill.sp_in_skill = getSpInSkill(
                char_skill[0].active_skill_level, skill.skill_type
            )

        total_sp += farming_skill.sp_in_skill
        farming_skill.save()

    for skill in char_farm_skills:
        if skill.skill_type_id not in [f_s.skill_id for f_s in farming_skills]:
            skill.delete()

    farm_character.total_large_extractors = total_sp / 510000
    farm_character.last_update = datetime.datetime.now(datetime.timezone.utc)
    farm_character.save()
