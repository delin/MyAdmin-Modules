__author__ = 'delin'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'modules.ftp.views.main', name='main'),
    # url(r'^logout/$', 'app_accounts.views.page_logout', name='logout'),
)