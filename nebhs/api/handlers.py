from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
from google.appengine.ext import db
from nebhs.models import Animal, AnimalPhoto
from django.core.urlresolvers import reverse
from nebhs import settings
from gae_memoize.memoize import memoize,default_keygen

import logging

def query_keygen(*args,**kwargs):
    kwargs.update(dict(args[1]))
    return default_keygen(**kwargs)

#@memoize(3600,keygen=query_keygen,force_cache=True)
def api_query(cls, params,limit=20):
    b = db.Query(cls)
    for k,v in params:
        if v:
            b = b.filter(k,v)
    return b.fetch(limit)

class AnimalHandler(BaseHandler):
    """
    Authenticated entrypoint for animals.
    """
    model = Animal
    allowed_methods = ('GET',)
    anonymous = 'AnonymousAnimalHandler'
    fields = ('name', 'code','gender','spayed_or_neutered',
        'main_color','breed','age','age_str','brought_to_shelter',
        'status','located_at','description','category','url',
        'img_uri','img_uri_full','meet_your_match','youtube_video_url',
        'petharbor_url','last_checked','uri')

    @classmethod
    def img_uri(cls,animal):
        try:
            return reverse('image_serve_scaled',
                    kwargs=dict(
                        image_key=animal.photo.key(),
                        extension='png',
                        width='220',
                        height='220'))
        except:
            return settings.DEFAULT_IMAGE_UNAVAILABLE

    @classmethod
    def img_uri_full(cls,animal):
        try:
            return reverse('image_serve_scaled',
                    kwargs=dict(
                        image_key=animal.photo.key(),
                        extension='png',
                        width='440',
                        height='440'))
        except:
            return settings.DEFAULT_IMAGE_UNAVAILABLE

    @classmethod
    def uri(cli,animal):
        return animal.get_absolute_url()

    def read(self, request, category=None, code=None, status='adoptable',
        meet_your_match=None):
        """
        Returns an animal, if `id` is given,
        otherwise all the posts.

        Parameters:
         - `title`: The title of the post to retrieve.
        """
        filter_set = [
            ('status =',status or request.GET.get('status')),
            ('category =',category or request.GET.get('category')),
            ('code =',code or request.GET.get('code')),
            ('meet_your_match =', meet_your_match or request.GET.get('meet_your_match'))
        ]
        return api_query(Animal,filter_set,70)

class AnonymousAnimalHandler(AnimalHandler, AnonymousBaseHandler):
    """
    Anonymous entrypoint for animals.
    """
    fields = ('name', 'code','gender','spayed_or_neutered','main_color',
    'breed','age','brought_to_shelter','status',
    'located_at','description','category',)
