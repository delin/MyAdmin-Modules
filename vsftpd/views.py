from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext as _
from MyAdmin.functions import prepare_data
from system_tools.services import SystemServices
from modules.vsftpd import myadmin_module
from modules.vsftpd.parser import vsFTPdParser


@login_required
@require_http_methods(["GET", "POST"])
def main(request):
    page_title = _("Info")

    config = vsFTPdParser()
    options = config.options()
    users = config.get_ftp_users()

    c = {}
    c.update(csrf(request))

    if 'POST' in request.method:
        if 'btn-reload' in request.POST:
            system_services = SystemServices()

            if system_services.reload("vsftpd"):
                messages.success(request,  _("Service reloaded"))
            else:
                messages.error(request,  _("Service reloaded error"))

        return redirect('module-vsftpd_main')

    config_options = []
    for option in options:
        config_options.append({
            "name": option,
            "value": config.get(option),
            "default": config.default_values.get(option),
        })

    system_services = SystemServices()
    service_status = system_services.status('vsftpd')

    return render(request, "main.html", {
        'loaded_module': myadmin_module,
        'page_title': page_title,
        'data': prepare_data(request),
        'config_options': config_options,
        'users': users,
        'service_status': service_status,
    })


@login_required
@require_http_methods(["GET", "POST"])
def edit(request):
    page_title = _("Edit")

    c = {}
    c.update(csrf(request))

    config = vsFTPdParser()

    if request.method == "POST":
        if request.POST.get('anonymous_enable'):
            config.set('anonymous_enable', 'YES')
        else:
            config.set('anonymous_enable', 'NO')

        if request.POST.get('anon_upload_enable'):
            config.set('anon_upload_enable', 'YES')
        else:
            config.set('anon_upload_enable', 'NO')

        if request.POST.get('anon_mkdir_write_enable'):
            config.set('anon_mkdir_write_enable', 'YES')
        else:
            config.set('anon_mkdir_write_enable', 'NO')

        if request.POST.get('local_enable'):
            config.set('local_enable', 'YES')
        else:
            config.set('local_enable', 'NO')

        if request.POST.get('write_enable'):
            config.set('write_enable', 'YES')
        else:
            config.set('write_enable', 'NO')

        if request.POST.get('listen'):
            config.set('listen', 'YES')
        else:
            config.set('listen', 'NO')

        if request.POST.get('listen_ipv6'):
            config.set('listen_ipv6', 'YES')
        else:
            config.set('listen_ipv6', 'NO')

        if request.POST.get('local_umask'):
            config.set('local_umask', request.POST.get('local_umask'))

        config.write()
        return redirect('module-vsftpd_main')

    return render(request, "edit.html", {
        'loaded_module': myadmin_module,
        'page_title': page_title,
        'data': prepare_data(request),
        'configs': config.get_configs_array(),
    })


@login_required
@require_http_methods(["GET", "POST"])
def user_add(request):
    page_title = _("Create new FTP user")

    c = {}
    c.update(csrf(request))

    return render(request, "user_add.html", {
        'loaded_module': myadmin_module,
        'page_title': page_title,
        'data': prepare_data(request),
    })