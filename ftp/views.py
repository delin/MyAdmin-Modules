from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext as _
from MyAdmin.functions import prepare_data
from modules.ftp.parser import vsFTPdParser


@login_required
@require_http_methods(["GET"])
def main(request):
    page_title = _("Info")

    config = vsFTPdParser()
    options = config.options()

    config_options = []
    for option in options:
        config_options.append({
            "name": option,
            "value": config.get(option),
            "default": config.default_values.get(option),
        })

    return render(request, "main.html", {
        'page_title': page_title,
        'data': prepare_data(request),
        'config_options': config_options,
    })


@login_required
@require_http_methods(["GET"])
def edit(request):
    page_title = _("Edit")

    config = vsFTPdParser()
    options = config.options()

    config_options = []
    for option in options:
        config_options.append({
            "name": option,
            "value": config.get(option),
            "default": config.default_values.get(option),
        })

    return render(request, "edit.html", {
        'page_title': page_title,
        'data': prepare_data(request),
        'config_options': config_options,
    })
