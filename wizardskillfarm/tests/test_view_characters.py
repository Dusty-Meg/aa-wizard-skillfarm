"""
Example Test
"""

# Django
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership, UserProfile
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils

from .. import models as local_models

# from .. import views as local_views


class TestExample(TestCase):
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

        cls.users = []
        cls.characters = []
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
            local_models.FarmingCharacters.objects.create(
                character=main_char,
                user=user,
                total_extract_sp=uid,
                total_large_extractors=uid + 2,
            )

            for skills in range(1, 4):
                local_models.CharacterFarmingSkill.objects.create(
                    character=main_char, skill_id=skills
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

    def test_example(self):
        login = self.client.login(username="User_2", password="Password_2")
        print(login)

        page = self.client.get(reverse("wizard-skillfarm:characters"))

        print(page)
        print(page.context["model"])

        self.assertEqual(True, True)
