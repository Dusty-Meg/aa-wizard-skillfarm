"""Task function tests."""

# Standard Library
from types import SimpleNamespace

# Django
from django.test import SimpleTestCase

from ..tasks import getSpInSkill


class TestGetSpInSkill(SimpleTestCase):
    def _mock_skill(self, rank_value):
        class DogmaQuery:
            def __init__(self, value):
                self._value = value

            def first(self):
                if self._value is None:
                    return None
                return SimpleNamespace(value=self._value)

        class DogmaManager:
            def __init__(self, value):
                self._value = value

            def filter(self, **kwargs):
                if kwargs.get("dogma_attribute_id") != 275:
                    return DogmaQuery(None)
                return DogmaQuery(self._value)

        return SimpleNamespace(dogma=DogmaManager(rank_value))

    def test_returns_sp_for_each_level(self):
        skill = self._mock_skill(rank_value=3)

        self.assertEqual(getSpInSkill(1, skill), 768)
        self.assertEqual(getSpInSkill(2, skill), 4242)
        self.assertEqual(getSpInSkill(3, skill), 24000)
        self.assertEqual(getSpInSkill(4, skill), 135765)
        self.assertEqual(getSpInSkill(5, skill), 768000)

    def test_returns_zero_for_unknown_level(self):
        skill = self._mock_skill(rank_value=2)

        self.assertEqual(getSpInSkill(0, skill), 0)

    def test_returns_zero_when_rank_dogma_is_missing(self):
        skill = self._mock_skill(rank_value=None)

        self.assertEqual(getSpInSkill(5, skill), 0)
