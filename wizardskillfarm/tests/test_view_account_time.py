"""
Example Test
"""

# Standard Library
from datetime import datetime, timedelta, timezone

# Django
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership, UserProfile
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils

from .. import models as local_models

# from corptools.models import CharacterAudit, EveItemType, SkillQueue


class TestViewAccountTime(TestCase):
    """
    Test View Account Time
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = RequestFactory()
        UserProfile.objects.all().delete()
        EveCharacter.objects.all().delete()
        local_models.AccountTimes.objects.all().delete()
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
            local_models.AccountTimes.objects.create(
                character=main_char,
                user=user,
                type="Plex",
                expiry=(datetime.utcnow() + timedelta(days=40)).replace(
                    tzinfo=timezone.utc
                ),
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

    def test_can_get_model(self):
        self.client.login(username="User_2", password="Password_2")

        page = self.client.get(reverse("wizard-skillfarm:omega_time"))

        context = page.context["model"]

        self.assertEqual(len(context.characters), 1)
        self.assertEqual(context.characters[0].type, "Plex")
