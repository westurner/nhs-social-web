# -*- coding: utf-8 -*-
from django.db.models import permalink,signals
from django.template.defaultfilters import pluralize
from google.appengine.ext import db
from google.appengine.api import images, urlfetch
import logging
from gaegene.image.models import *

ANIMAL_CATEGORIES = {'cats':'Cats and Kittens', 'dogs':'Dogs and Puppies','other':'Other Animals'}

class AnimalPhoto(GeneImage):
    @classmethod
    def create(
            cls, name, image_bytes=None, image_url=None,
            master=None, width=None, height=None, encoding=None,
            key_name=None
        ):
        image = None
        try:
            if image_bytes is None and image_url is not None:
                image_bytes = urlfetch.fetch(image_url).content
            # Make it square if we only have one dimension
            width = width or height
            height = height or width
            # Get the image_bytes meta-data
            data_info = image_info(image_bytes)
            data_encoding = data_info[0]
            data_width = data_info[1]
            data_height = data_info[2]
            try:
                width = new_width = int(width)
                if data_width and new_width > data_width:
                    new_width = data_width
            except:
                width = new_width = data_width
            new_height = height
            try:
                height = new_height = int(height)
                if data_height and new_height > data_height:
                    new_height = data_height
            except:
                height = new_height = data_height
            new_encoding = encoding
            if new_encoding is None:
                new_encoding = data_encoding
            # Make it square if we only have one dimension
            new_width = new_width or new_height
            new_height = new_height or new_width
            # Can't resize if we don't have encoding and dimension
            if new_encoding is not None and new_width is not None:
                # Should we resize/reencode?
                if ((new_encoding != data_encoding) or
                    (new_width != data_width) or
                    (new_height != data_height)):
                    image_bytes = images.resize(
                        image_bytes,
                        width=new_width,
                        height=new_height,
                        output_encoding=new_encoding
                    )
                # Grab the new image info
                temp_image = images.Image(image_bytes)
                data_width = temp_image.width
                data_height = temp_image.height
            image = AnimalPhoto(
                name=name,
                image_bytes=image_bytes,
                image_url=image_url,
                master=master,
                requested_width=width,
                requested_height=height,
                actual_width=data_width,
                actual_height=data_height,
                encoding=new_encoding,
                key_name=key_name
            )
            image.put()
        except Exception, e:
            logging.error("Failed to create image: %s" % str(e))
            if image and image.is_saved():
                try:
                    image.delete()
                except Exception, e2:
                    logging.error(
                        "Failed to delete error image: %s" % str(e2)
                    )
                image = None
        return image
    pass

class Animal(db.Model):
    name = db.StringProperty(required=True)
    code = db.StringProperty(required=True)
    gender = db.StringProperty()
    spayed_or_neutered = db.StringProperty()
    main_color = db.StringProperty()
    breed = db.StringProperty()
    age = db.FloatProperty()
    brought_to_shelter = db.DateProperty(required=True)
    #created = db.DateTimeProperty()
    #modified = db.DateTimeProperty()
    
    status = db.StringProperty() #choices = set(['adoptable','expired'])
    located_at = db.StringProperty()
    description = db.TextProperty()

    category = db.StringProperty() #Category(choices = set(["cat","dog","oo"])) #
    photo = db.ReferenceProperty(AnimalPhoto) #BlobProperty()

    last_checked = db.DateTimeProperty()    
    petharbor_url = db.LinkProperty()    

    def __str__(self):
        return '[%s] %s' % (self.code,self.name)

    @permalink
    def get_absolute_url(self):
        return ('nebhs.views.show_animal_by_name', (), {'category':self.category,
            'name':self.name,
            'year':self.brought_to_shelter.year,
            'month':self.brought_to_shelter.month,
            'day':self.brought_to_shelter.day})

    def age_str(self):
        total = self.age * 12
        years = int(total // 12)
        months = int(total % 12)
        yr = "%s year%s" % (years, pluralize(years))
        mn = "%s month%s" % (months, pluralize(months))
        if years and months:
            return ', '.join((yr, mn))
        elif months:
            return mn
        elif yr:
            return yr
        else:
            return None

    def gender_str(self):
        if self.gender.lower()=="male":
            return "he"
        if self.gender.lower()=="female":
            return "she"
        else:
            return self.name