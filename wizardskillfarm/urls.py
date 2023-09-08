"""App URLs"""

# Django
from django.urls import path

# AA Wizard Skill Farm
from wizardskillfarm import views

app_name: str = "wizard-skillfarm"

urlpatterns = [
    path("", views.index, name="index"),
    path("characters/", views.characters, name="characters"),
]
