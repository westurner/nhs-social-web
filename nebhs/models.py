# -*- coding: utf-8 -*-
from django.db.models import permalink,signals
from django.template.defaultfilters import pluralize
from google.appengine.ext import db
from gaegene.image.models import GeneImage

ANIMAL_CATEGORIES = {'cats':'Cats and Kittens', 'dogs':'Dogs and Puppies','other':'Other Animals'}

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
    photo = db.ReferenceProperty(GeneImage) #BlobProperty()

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
            return "unknown"

    def gender_str(self):
        if self.gender.lower()=="male":
            return "he"
        if self.gender.lower()=="female":
            return "she"
        else:
            return "it"