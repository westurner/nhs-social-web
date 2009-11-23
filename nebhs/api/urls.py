from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view

from nebhs.api.handlers import AnimalHandler

animals = Resource(handler=AnimalHandler)

urlpatterns = patterns('',
    url(r'^animals/$', animals),
    url(r'^animals/(?P<emitter_format>[\w]+)/$', animals),
    url(r'^animals/(?P<emitter_format>[\w]+)/(?P<category>[dogs|cats|other]+)/$', animals),
    url(r'^animals\.(?P<emitter_format>[\w]+)/(?P<category>[dogs|cats|other]+)/$', animals),
    url(r'^animals\.(?P<emitter_format>[\w]+)', animals),

    # automated documentation
    url(r'^$', documentation_view),
)