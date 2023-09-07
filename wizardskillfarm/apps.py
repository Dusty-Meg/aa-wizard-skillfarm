"""App Configuration"""

# Django
from django.apps import AppConfig

# AA Wizard Skill Farm
from wizardskillfarm import __version__


class WizardSkillFarmConfig(AppConfig):
    """App Config"""

    name = "wizardskillfarm"
    label = "wizardskillfarm"
    verbose_name = f"Wizard Skill Farm v{__version__}"
