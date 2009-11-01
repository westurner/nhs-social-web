# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response


# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
from google.appengine.ext import db
from mimetypes import guess_type
from nebhs.forms import AnimalForm
from nebhs.models import Animal, ANIMAL_CATEGORIES
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
import datetime


def _animal_page_title(a):
    if a.breed:
        return "%s the %s: %s - Adoptable %s" % (a.name.capitalize(), a.breed, a.brought_to_shelter.strftime("%m/%d/%Y"), a.category.capitalize())
    return "%s: %s - Adoptable %s" % (a.name.capitalize(), a.brought_to_shelter.strftime("%m/%d/%Y"), a.category.capitalize())

def list_animals(request, category):
    if category not in ANIMAL_CATEGORIES.keys():
        raise Exception
    return object_list(request, db.Query(Animal).filter('category =',category).filter('status =','adoptable').order('-brought_to_shelter'), paginate_by=15, extra_context={'page_title':ANIMAL_CATEGORIES[category]})

def show_animal_by_id(request, category, id):
    a = animal = get_object_or_404(Animal, 'category =', category, 'code = ', id) # todo: also check date
    return render_to_response(request, "nebhs/animal_detail.html",
        data={'object':animal,
            'page_title':_animal_page_title(animal)
        }) #Adoptable {{ object.category|capfirst }}: {{ object.name|capfirst }}
    pass

def show_animal_by_name(request, category, year, month, day, name):

    date_ = datetime.date(int(year),int(month),int(day))
    a = animal = get_object_or_404(Animal, 'brought_to_shelter =', date_, 'category =', category, 'name = ', name) # todo: also check date
    return render_to_response(request, "nebhs/animal_detail.html",
        data={'object':animal,
            'page_title':_animal_page_title(animal)
        })
    #return object_detail(request, db.Query(Animal).all(), key)

def show_animal(request, key):
    return object_detail(request, Animal.all(), key)



def download_file(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')

def create_admin_user(request):
    user = User.get_by_key_name('admin')
    if not user or user.username != 'admin' or not (user.is_active and
            user.is_staff and user.is_superuser and
            user.check_password('admin')):
        user = User(key_name='admin', username='admin',
            email='admin@localhost', first_name='Boss', last_name='Admin',
            is_active=True, is_staff=True, is_superuser=True)
        user.set_password('admin')
        user.put()
    return render_to_response(request, 'nebhs/admin_created.html')
