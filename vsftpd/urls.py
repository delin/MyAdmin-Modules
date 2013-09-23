__author__ = 'delin'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'modules.vsftpd.views.main', name='module-vsftpd_main'),
    url(r'^edit/$', 'modules.vsftpd.views.edit', name='module-vsftpd_edit'),
    url(r'^user_add/$', 'modules.vsftpd.views.user_add', name='module-vsftpd_user_add'),
)
