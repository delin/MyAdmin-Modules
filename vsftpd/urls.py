__author__ = 'delin'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'modules.ftp.views.main', name='module-vsftpd_main'),
    url(r'^edit/$', 'modules.ftp.views.edit', name='module-vsftpd_edit'),
)
