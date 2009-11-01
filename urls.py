# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from nebhs.urls import urlpatterns as nebhs_patterns
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
    ('^admin/(.*)', admin.site.root),
    #(r'^$', 'django.views.generic.simple.direct_to_template',
    #    {'template': 'main.html'}),
    (r'^adopt/',  include('nebhs.urls'))
    # Override the default registration form
) + urlpatterns
