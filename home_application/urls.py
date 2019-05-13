# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^bean-api/(?P<vm_id>[0-9]+)/$', 'vcenter'),
    (r'^bean-api/$', 'add_vm'),
    (r'^bean-api/vminfo/$', 'get_vminfo')

)
