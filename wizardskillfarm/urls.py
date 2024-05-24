"""App URLs"""

# Django
from django.urls import path

# AA Wizard Skill Farm
from wizardskillfarm import views

app_name: str = "wizard-skillfarm"

urlpatterns = [
    path("", views.index, name="index"),
    path("characters/", views.characters, name="characters"),
    path("omegatime/", views.omega_time, name="omegatime"),
    path("settings/characters", views.settings_characters, name="settings_characters"),
    path("settings/skills", views.settings_skills, name="settings_skills"),
    path("settings/omegatime", views.settings_omegatime, name="settings_omegatime"),
]
