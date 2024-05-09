"""App URLs"""

# Django
from django.urls import path

# AA Wizard Skill Farm
from wizardskillfarm import views

app_name: str = "wizard-skillfarm"

urlpatterns = [
    path("", views.index, name="index"),
    path("characters/", views.characters, name="characters"),
    path("omega_time/", views.omega_time, name="omega_time"),
    path("settings/characters", views.settings_characters, name="settings_characters"),
]
