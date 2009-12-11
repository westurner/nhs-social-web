# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
    (r'^facebook/xd_receiver.htm/$', direct_to_template, {'template':'fb/xd_receiver.htm'}),
    ('^admin/(.*)', admin.site.root),
    (r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'nebhs/main.html'}),
    (r'^adopt/',  include('nebhs.urls')),
    (r'^adopt/api/',  include('nebhs.api.urls'))
    # Override the default registration form
) + urlpatterns
