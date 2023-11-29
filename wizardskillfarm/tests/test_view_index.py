"""
Example Test
"""

# Standard Library
from datetime import datetime, timedelta, timezone

# Third Party
from corptools.models import CharacterAudit, SkillQueue

# Django
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership, UserProfile
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils

from .. import models as local_models


class TestViewIndex(TestCase):
    """
    Test View Index
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
        cls.char_audits = []

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
                total_large_extractors=uid + 2,
            )

            char_audit = CharacterAudit.objects.create(active=True, character=main_char)

            for skills in range(1, 4):
                SkillQueue.objects.create(
                    character=char_audit,
                    finish_level=skills,
                    queue_position=skills,
                    skill_id=23,
                    finish_date=(datetime.utcnow() + timedelta(days=3)).replace(
                        tzinfo=timezone.utc
                    ),
                    start_date=(datetime.utcnow() + timedelta(days=1)).replace(
                        tzinfo=timezone.utc
                    ),
                )

            cls.char_audits.append(char_audit)

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

    def test_can_get_model_with_low_skills(self):
        self.client.login(username="User_2", password="Password_2")

        page = self.client.get(reverse("wizard-skillfarm:index"))

        context = page.context["model"]

        self.assertEqual(len(context.low_skill_queue), 1)
        self.assertEqual(len(context.paused_skill_queue), 0)

    def test_can_get_model_with_paused_skills(self):
        SkillQueue.objects.all().delete()

        audit = self.char_audits[1]

        for skills in range(1, 4):
            SkillQueue.objects.create(
                character=audit,
                finish_level=skills,
                queue_position=skills,
                skill_id=23,
                finish_date=(datetime.utcnow() + timedelta(days=3)).replace(
                    tzinfo=timezone.utc
                ),
                start_date=(datetime.utcnow() + timedelta(days=1)).replace(
                    tzinfo=timezone.utc
                ),
            )
        SkillQueue.objects.create(
            character=audit,
            finish_level=5,
            queue_position=4,
            skill_id=23,
            start_date=(datetime.utcnow() - timedelta(days=4)).replace(
                tzinfo=timezone.utc
            ),
        )

        self.client.login(username="User_2", password="Password_2")

        page = self.client.get(reverse("wizard-skillfarm:index"))

        context = page.context["model"]

        self.assertEqual(len(context.low_skill_queue), 0)
        self.assertEqual(len(context.paused_skill_queue), 1)

    def test_can_get_model_with_old_paused_skills(self):
        SkillQueue.objects.all().delete()

        audit = self.char_audits[1]

        for skills in range(1, 4):
            SkillQueue.objects.create(
                character=audit,
                finish_level=skills,
                queue_position=skills,
                skill_id=23,
                finish_date=(datetime.utcnow() + timedelta(days=3)).replace(
                    tzinfo=timezone.utc
                ),
                start_date=(datetime.utcnow() + timedelta(days=1)).replace(
                    tzinfo=timezone.utc
                ),
            )
        SkillQueue.objects.create(
            character=audit,
            finish_level=5,
            queue_position=4,
            skill_id=23,
            start_date=(datetime.utcnow() - timedelta(days=91)).replace(
                tzinfo=timezone.utc
            ),
        )

        self.client.login(username="User_2", password="Password_2")

        page = self.client.get(reverse("wizard-skillfarm:index"))

        context = page.context["model"]

        self.assertEqual(len(context.low_skill_queue), 0)
        self.assertEqual(len(context.paused_skill_queue), 0)
