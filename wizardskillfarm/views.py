"""App Views"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# from .models import *
from .view_models import characters_character, characters_main


@login_required
@permission_required("wizardskillfarm.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    context = {"text": "Hello, World!"}

    return render(request, "example/index.html", context)


@login_required
# @permission_required("wizardskillfarm.basic_access")
def characters(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    view_model = characters_main()

    context_2 = request.user.farmingcharacters.all()

    for char in context_2:
        view_char = characters_character()
        view_char.name = char.character.character_name
        view_char.last_update = char.last_update
        view_char.total_extract_sp = char.total_extract_sp
        view_char.total_large_extractors = char.total_large_extractors
        view_model.characters.append(view_char)

    context = {"model": view_model}

    return render(request, "example/index.html", context)
