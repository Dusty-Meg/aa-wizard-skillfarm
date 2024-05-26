"""App Views"""

# Standard Library
from datetime import datetime, timedelta, timezone

# Third Party
from corptools.models import CharacterAudit, SkillQueue

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register

# Alliance Auth (External Libs)
from eveuniverse.models import EveType

from .models import AccountTimes, FarmingCharacters, FarmingSkills

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
    settings_omegatime_character,
    settings_omegatime_main,
    settings_skills_main,
    settings_skills_skill,
)


@register.filter
def get_range(stop):
    return range(0, stop)


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
    farming_skills = request.user.farmingskills.all()
    farming_omega = request.user.accounttimes.all()

    view_model.has_characters = farming_characters
    view_model.has_skills = farming_skills
    view_model.has_omega = farming_omega

    for character in farming_characters:
        last_skill = SkillQueue.objects.filter(character__character=character.character)

        if not last_skill:
            continue

        last_skill = last_skill.latest("queue_position")

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
            view_skill.skill_id = skill.skill_type.id
            view_skill.skill_name = skill.skill_type.name
            view_skill.skill_level = skill.skill_level
            view_skill.sp_in_skill = skill.sp_in_skill
            view_char.skills.append(view_skill)

        view_model.characters.append(view_char)

    view_model.characters = sorted(
        view_model.characters, key=lambda x: x.name, reverse=False
    )

    context = {"model": view_model}

    return render(request, "wizardskillfarm/characters.html", context)


def calculate_remaining(expiry):
    # Calculate remaining time
    remaining_time = expiry - datetime.now(timezone.utc)
    days, remainder = divmod(remaining_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    # Format remaining time into a string
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"


@login_required
@permission_required("wizardskillfarm.basic_access")
def omega_time(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    if request.method == "POST":
        account_times = AccountTimes.objects.filter(user=request.user).filter(
            character__character_id=request.POST.get("characterId")
        )

        if account_times is not None and len(account_times) == 1:
            new_expiry = datetime.strptime(
                f"{request.POST.get('date')} {request.POST.get('time')}",
                "%Y-%m-%d %H:%M",
            )
            account_times[0].expiry = new_expiry + timedelta(
                days=(int(request.POST.get("units")) * 30)
            )
            account_times[0].save()
        return HttpResponse(status=200)

    view_model = account_time_main()

    account_times = AccountTimes.objects.filter(user=request.user)

    for char in account_times:
        view_char = account_time_character()
        view_char.name = char.character.character_name
        view_char.id = char.character.character_id
        view_char.type = char.type
        view_char.expiry = char.expiry
        view_char.remaining = calculate_remaining(char.expiry)

        view_model.characters.append(view_char)

    view_model.characters = sorted(
        view_model.characters, key=lambda x: x.expiry, reverse=False
    )

    context = {"model": view_model}

    return render(request, "wizardskillfarm/omegatime.html", context)


@login_required
@permission_required("wizardskillfarm.basic_access")
def settings_characters(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        included_characters = FarmingCharacters.objects.filter(user=request.user)
        all_characters = CharacterAudit.objects.visible_to(request.user).filter(
            character__userprofile__user_id=request.user.id
        )

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

    all_characters = CharacterAudit.objects.visible_to(request.user).filter(
        character__userprofile__user_id=request.user.id
    )
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


@login_required
@permission_required("wizardskillfarm.basic_access")
def settings_skills(request: WSGIRequest) -> HttpResponse:

    if request.method == "POST":
        all_skills = (
            EveType.objects.filter(icon_id=33)
            .filter(published=True)
            .filter(eve_market_group__isnull=False)
        )
        included_skills = FarmingSkills.objects.filter(user=request.user)

        post_data = request.POST.getlist("to")

        for included_skill in included_skills:
            found = False
            for post_skills in post_data:
                if included_skill.skill_type.name == post_skills:
                    found = True
            if not found:
                FarmingSkills.objects.filter(skill_id=included_skill.skill_id).delete()

        for post_skills in post_data:
            for included_skill in all_skills:
                if included_skill.name == post_skills:
                    skills, created = FarmingSkills.objects.get_or_create(
                        skill_id=included_skill.id,
                        user=request.user,
                        skill_type=included_skill,
                    )

                    if created:
                        skills.save()
        return redirect("/wizard-skillfarm/settings/skills")

    all_skills = (
        EveType.objects.filter(icon_id=33)
        .filter(published=True)
        .filter(eve_market_group__isnull=False)
    )
    included_skills = FarmingSkills.objects.filter(user=request.user)

    view_model = settings_skills_main()

    for skill in all_skills:
        model = settings_skills_skill()
        model.name = skill.name
        model.id = skill.id

        found = False
        for included_skill in included_skills:
            if model.id == included_skill.skill_id:
                found = True

        if found is False:
            view_model.not_included_skills.append(model)

    for skill in included_skills:
        model = settings_skills_skill()
        model.name = skill.skill_type.name
        model.id = skill.id
        view_model.included_skills.append(model)

    context = {"model": view_model}

    return render(request, "wizardskillfarm/settings/skills.html", context)


@login_required
@permission_required("wizardskillfarm.basic_access")
def settings_omegatime(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        all_characters = CharacterAudit.objects.visible_to(request.user).filter(
            character__userprofile__user_id=request.user.id
        )
        account_times = AccountTimes.objects.filter(user=request.user)

        post_data_omega = request.POST.getlist("to")
        post_data_mct = request.POST.getlist("to_2")

        for included_char in account_times:
            found = False
            for post_characters in post_data_omega:
                if included_char.character.character_name == post_characters:
                    found = True
            for post_characters in post_data_mct:
                if included_char.character.character_name == post_characters:
                    found = True
            if not found:
                AccountTimes.objects.filter(character=included_char.character).delete()

        for post_characters in post_data_omega:
            for included_char in all_characters:
                if included_char.character.character_name == post_characters:
                    character, created = AccountTimes.objects.get_or_create(
                        character_id=included_char.character_id,
                        defaults={
                            "character": included_char.character,
                            "user": request.user,
                            "type": "omega",
                            "expiry": datetime.now(timezone.utc),
                        },
                    )

                    if created:
                        character.save()

        for post_characters in post_data_mct:
            for included_char in all_characters:
                if included_char.character.character_name == post_characters:
                    character, created = AccountTimes.objects.get_or_create(
                        character_id=included_char.character_id,
                        defaults={
                            "character": included_char.character,
                            "user": request.user,
                            "type": "mct",
                            "expiry": datetime.now(timezone.utc),
                        },
                    )

                    if created:
                        character.save()
        return redirect("/wizard-skillfarm/settings/omegatime")

    all_characters = CharacterAudit.objects.visible_to(request.user).filter(
        character__userprofile__user_id=request.user.id
    )
    account_times = AccountTimes.objects.filter(user=request.user)

    view_model = settings_omegatime_main()

    for char in all_characters:
        model = settings_omegatime_character()
        model.name = char.character.character_name
        model.id = char.character.character_id

        found = False
        for included_char in account_times:
            if model.id == included_char.character.character_id:
                found = True

        if found is False:
            view_model.not_included_characters.append(model)

    for char in account_times:
        model = settings_omegatime_character()
        model.name = char.character.character_name
        model.id = char.character.character_id

        if char.type == "omega":
            view_model.omega_characters.append(model)
        elif char.type == "mct":
            view_model.mct_characters.append(model)

    context = {"model": view_model}

    return render(request, "wizardskillfarm/settings/omegatime.html", context)
