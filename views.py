from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext as _
from MyAdmin.functions import prepare_data


@login_required
@require_http_methods(["GET"])
def main(request):
    page_title = _("Info")

    return render(request, "main.html", {
        'page_title': page_title,
        'data': prepare_data(request),
    })