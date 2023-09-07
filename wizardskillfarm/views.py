"""App Views"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# from .models import *


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
@permission_required("wizardskillfarm.basic_access")
def characters(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    request.user.farmingcharacters

    context = {"text": "Hello, World!"}

    return render(request, "example/index.html", context)
