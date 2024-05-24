"""
Example Test
"""

# Third Party

# Django
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership, UserProfile
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils

# Alliance Auth (External Libs)
from eveuniverse.models import EveType

from .. import models as local_models


class TestViewCharacter(TestCase):
    """
    Test View Character
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = RequestFactory()
        UserProfile.objects.all().delete()
        EveCharacter.objects.all().delete()
        local_models.FarmingCharacters.objects.all().delete()
        User.objects.all().delete()

        userids = range(1, 4)

        cls.users = []
        cls.characters = []

        skill_types = []

        for skill_item in range(3340, 3344):
            skill_types.append(
                EveType.objects.create(
                    id=skill_item,
                    name=f"Teapot Test {skill_item}",
                    published=True,
                    eve_group_id=2,
                )
            )

        for uid in userids:
            user = User.objects.create(username=f"User_{uid}")
            user.set_password(f"Password_{uid}")
            user.save()
            main_char = AuthUtils.add_main_character_2(
                user,
                f"Main {uid}",
                uid,
                corp_id=1,
                corp_name="Test Corp 1",
                corp_ticker="TST1",
            )
            CharacterOwnership.objects.create(
                user=user, character=main_char, owner_hash=f"main{uid}"
            )
            local_farming_character = local_models.FarmingCharacters.objects.create(
                character=main_char,
                user=user,
                total_large_extractors=uid + 2,
            )

            for skills in range(1, 4):
                local_models.CharacterFarmingSkill.objects.create(
                    character=main_char,
                    skill_type=skill_types[skills - 1],
                    skill_level=3,
                    sp_in_skill=200000,
                    farming_character=local_farming_character,
                )

            user = AuthUtils.add_permissions_to_user_by_name(
                [
                    "wizardskillfarm.basic_access",
                ],
                user,
            )
            user.save()

            cls.characters.append(main_char)
            cls.users.append(user)

        super().setUpClass()

    def test_can_get_model_with_full_context(self):
        self.client.login(username="User_2", password="Password_2")

        page = self.client.get(reverse("wizard-skillfarm:characters"))

        context = page.context["model"]

        self.assertEqual(len(context.characters), 1)
        self.assertEqual(context.characters[0].name, "Main 2")
        self.assertEqual(len(context.characters[0].skills), 3)
        self.assertEqual(context.characters[0].total_extract_sp(), 600000)

    def test_can_get_model_with_no_characters(self):
        local_models.FarmingCharacters.objects.all().delete()

        self.client.login(username="User_2", password="Password_2")

        page = self.client.get(reverse("wizard-skillfarm:characters"))

        context = page.context["model"]

        self.assertEqual(len(context.characters), 0)
