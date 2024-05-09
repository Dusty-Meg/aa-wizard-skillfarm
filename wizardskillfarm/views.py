"""App Views"""

# Standard Library
from datetime import datetime, timezone

# Third Party
from corptools.models import CharacterAudit, SkillQueue

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import FarmingCharacters

# from .models import *
from .view_models import (
    account_time_character,
    account_time_main,
    characters_character,
    characters_character_skill,
    characters_main,
    index_main,
    index_skill_queue,
    settings_characters_character,
    settings_characters_main,
)


@login_required
@permission_required("wizardskillfarm.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    view_model = index_main()

    farming_characters = request.user.farmingcharacters.all()

    for character in farming_characters:
        last_skill = SkillQueue.objects.filter(
            character__character=character.character
        ).latest("queue_position")

        days_between_now_and_start = (
            datetime.now(timezone.utc) - last_skill.start_date
            if last_skill.start_date is not None
            else 9000
        )

        if last_skill.finish_date is not None:
            days_between_now_and_end = (
                datetime.now(timezone.utc) - last_skill.finish_date
            )

            if (
                days_between_now_and_end.days > -7
                and days_between_now_and_end.days < 25
            ):
                skill_queue = index_skill_queue()
                skill_queue.name = character.character.character_name
                skill_queue.skill_queue_end = last_skill.finish_date
                view_model.low_skill_queue.append(skill_queue)
        elif (
            last_skill.finish_date is None
            and last_skill.start_date is not None
            and days_between_now_and_start.days < 90
        ):
            skill_queue = index_skill_queue()
            skill_queue.name = character.character.character_name
            skill_queue.skill_queue_end = last_skill.finish_date
            view_model.paused_skill_queue.append(skill_queue)

    context = {"model": view_model}

    return render(request, "wizardskillfarm/index.html", context)


@login_required
@permission_required("wizardskillfarm.basic_access")
def characters(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    view_model = characters_main()

    farming_characters = request.user.farmingcharacters.all()

    for char in farming_characters:
        view_char = characters_character()
        view_char.name = char.character.character_name
        view_char.last_update = char.last_update
        view_char.total_large_extractors = char.total_large_extractors

        for skill in char.farming_skills.all():
            view_skill = characters_character_skill()
            view_skill.skill_id = skill.skill_type.type_id
            view_skill.skill_name = skill.skill_type.name
            view_skill.skill_level = skill.skill_level
            view_skill.sp_in_skill = skill.sp_in_skill
            view_char.skills.append(view_skill)

        view_model.characters.append(view_char)

    context = {"model": view_model}

    return render(request, "wizardskillfarm/characters.html", context)


@login_required
@permission_required("wizardskillfarm.basic_access")
def omega_time(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    view_model = account_time_main()

    account_times = request.user.accounttimes.all()

    for char in account_times:
        view_char = account_time_character()
        view_char.name = char.character.character_name
        view_char.type = char.type
        view_char.expiry = char.expiry

        view_model.characters.append(view_char)

    context = {"model": view_model}

    return render(request, "wizardskillfarm/omegatime.html", context)


@login_required
@permission_required("wizardskillfarm.basic_access")
def settings_characters(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        included_characters = FarmingCharacters.objects.filter(user=request.user)
        all_characters = CharacterAudit.objects.visible_to(request.user)

        post_data = request.POST.getlist("to")

        for included_char in included_characters:
            found = False
            for post_characters in post_data:
                if included_char.character.character_name == post_characters:
                    found = True
            if not found:
                FarmingCharacters.objects.filter(
                    character=included_char.character
                ).delete()

        for post_characters in post_data:
            for included_char in all_characters:
                if included_char.character.character_name == post_characters:
                    character, created = FarmingCharacters.objects.get_or_create(
                        character_id=included_char.character_id,
                        defaults={
                            "character": included_char.character,
                            "user": request.user,
                            "total_large_extractors": 0,
                        },
                    )

                    if created:
                        character.save()
        return redirect("/wizard-skillfarm/settings/characters")

    all_characters = CharacterAudit.objects.visible_to(request.user)
    included_characters = FarmingCharacters.objects.filter(user=request.user)

    view_model = settings_characters_main()

    for char in all_characters:
        model = settings_characters_character()
        model.name = char.character.character_name
        model.id = char.character.character_id

        found = False
        for included_char in included_characters:
            if model.id == included_char.character.character_id:
                found = True

        if found is False:
            view_model.not_included_characters.append(model)

    for char in included_characters:
        model = settings_characters_character()
        model.name = char.character.character_name
        model.id = char.character.character_id
        view_model.included_characters.append(model)

    context = {"model": view_model}

    return render(request, "wizardskillfarm/settings/characters.html", context)
