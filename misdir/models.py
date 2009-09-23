# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from ragendja.dbutils import FakeModelListProperty
from google.appengine.ext import db
from django.contrib.auth.models import Permission

__doc__="""

TODO
=====
- Logos/Avatars
- Gaegee Slugs
"""

class Institution(db.Model):
    """
    This model stores the schools, along with their state and country
    (there seems to be cities with the same name, but located in
    different countries).

    This model also stores the geographic location of the city, which
    is calculated by an appengine CRON process.
    """
    name = db.StringProperty()
    address = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    zip_code = db.StringProperty()
    location = db.GeoPtProperty()

    owner = db.UserProperty()
    creation_date = db.DateTimeProperty(auto_now_add=True)
    modified_date = db.DateTimeProperty(auto_now=True)
    permissions = FakeModelListProperty(Permission)

    status = db.StringProperty()
    CHAPTER_STATES = ['pending_review','published']

    def __unicode__(self):
        return self.name


class StudentChapter(db.Model):
    """
    This model stores the student chapters
    """
    name = db.StringProperty(required=True)
    institution = db.ReferenceProperty(Institution,collection_name="student_chapters")
    aissc_member = db.BooleanProperty()

    facebook_page = db.LinkProperty()
    twitter_username = db.StringProperty()
    linkedin_group = db.LinkProperty()
    rss_feed = db.LinkProperty()
    website = db.LinkProperty()
    
    address = db.StringProperty(multiline=True)
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    zip_code = db.StringProperty()
    location = db.GeoPtProperty()

    owner = db.UserProperty()
    creation_date = db.DateTimeProperty(auto_now_add=True)
    modified_date = db.DateTimeProperty(auto_now=True)
    permissions = FakeModelListProperty(Permission)

    status = db.StringProperty()
    CHAPTER_STATES = ['pending_review','published']

    def __unicode__(self):
        return "%s" % (self.name)

class Degree(db.Model):
    """
    A degree offered by a school
    """
    institution = db.ReferenceProperty(Institution,collection_name="degrees")
    name = db.StringProperty()
    degree_type = db.StringProperty()
    DEGREE_TYPES = ["BA","BS","MBA","MS","PhD"]

    owner = db.UserProperty()
    creation_date = db.DateTimeProperty(auto_now_add=True)
    modified_date = db.DateTimeProperty(auto_now=True)
    permissions = FakeModelListProperty(Permission)

    status = db.StringProperty()
    CHAPTER_STATES = ['pending_review','published']

    def __unicode__(self):
        return "%s" % (self.name)

class Business(db.Model):
    """
    A business with demand for MIS
    """
    name = db.StringProperty(required=True)
    aissc_sponsor = db.BooleanProperty()
    # TODO: sponsor info
    #aissc_sponsor_level = db.StringProperty()
    #SPONSOR_TYPES = [...]

    facebook_page_url = db.LinkProperty()
    twitter_username = db.StringProperty()
    linkedin_group = db.StringProperty()
    rss_feed = db.LinkProperty()
    website = db.LinkProperty()

    # TODO: BusinessLocations
    address = db.StringProperty(multiline=True)
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    zip_code = db.StringProperty()
    location = db.GeoPtProperty()

    owner = db.UserProperty()
    creation_date = db.DateTimeProperty(auto_now_add=True)
    modified_date = db.DateTimeProperty(auto_now=True)
    permissions = FakeModelListProperty(Permission)

    status = db.StringProperty()
    CHAPTER_STATES = ['pending_review','published']

    def __unicode_(self):
        return self.name
