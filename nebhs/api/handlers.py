from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
from google.appengine.ext import db
from nebhs.models import Animal, AnimalPhoto
from django.core.urlresolvers import reverse
from nebhs import settings

class AnimalHandler(BaseHandler):
    """
    Authenticated entrypoint for animals.
    """
    model = Animal
    allowed_methods = ('GET',)
    anonymous = 'AnonymousAnimalHandler'
    fields = ('name', 'code','gender','spayed_or_neutered',
        'main_color','breed','age','brought_to_shelter',
        'status','located_at','description','category','url',
        'img_uri','meet_your_match','youtube_video_url',
        'petharbor_url','last_checked','uri')

    @classmethod
    def img_uri(cls,animal):
        try:
            return reverse('image_serve_scaled',kwargs=dict(image_key=animal.photo.key(),extension='png',width='220',height='220'))
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
        base = db.Query(Animal)

        if status or request.GET.get('status'):
            base = base.filter('status =',status or request.GET.get('status'))

        if category or request.GET.get('category'):
            base = base.filter('category =',category or request.GET.get('category'))

        if code or request.GET.get('code'):
            base = base.filter('code =',code or request.GET.get('code'))

        if meet_your_match or request.GET.get('meet_your_match'):
            # TODO: assign numeric constants to meet your match scale
            base = base.filter('meet_your_match =',meet_your_match or request.GET.get('meet_your_match'))

        return base.fetch(70)



class AnonymousAnimalHandler(AnimalHandler, AnonymousBaseHandler):
    """
    Anonymous entrypoint for animals.
    """
    fields = ('name', 'code','gender','spayed_or_neutered','main_color','breed','age','brought_to_shelter',
    'status','located_at','description','category',)
