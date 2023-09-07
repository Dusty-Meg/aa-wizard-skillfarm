"""
Example Test
"""

# Django
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership, UserProfile
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils

from .. import models as local_models

# from .. import views as local_views


class TestExample(TestCase):
    fixtures = ["disable_analytics"]
    """
    TestExample
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = RequestFactory()
        UserProfile.objects.all().delete()
        EveCharacter.objects.all().delete()
        local_models.FarmingCharacters.objects.all().delete()
        User.objects.all().delete()

        userids = range(1, 4)

        users = []
        characters = []
        for uid in userids:
            user = AuthUtils.create_user(f"User_{uid}")
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
            local_models.FarmingCharacters.objects.create(
                character=main_char,
                total_extract_sp=uid,
                total_large_extractors=uid + 2,
            )

            for skills in range(1, 4):
                local_models.CharacterFarmingSkill.objects.create(
                    character=main_char, skill_id=skills
                )

            characters.append(main_char)
            users.append(user)

        super().setUpClass()

    def test_example(self):
        self.app.set_user(self.users[0])

        page = self.app.get("/wizard-skillfarm/characters")

        print(page)

        self.assertEqual(True, True)
