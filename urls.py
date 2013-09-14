__author__ = 'delin'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'modules.ftp.views.main', name='module-ftp_main'),
    url(r'^edit/$', 'modules.ftp.views.edit', name='module-ftp_edit'),
    # url(r'^logout/$', 'app_accounts.views.page_logout', name='logout'),
)