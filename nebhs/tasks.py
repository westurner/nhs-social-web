#!/usr/bin/env python2.5
import datetime
#from common.appenginepatch.aecmd import setup_env
#setup_env(manage_py_env=True)

from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue
from google.appengine.api.labs.taskqueue import Task, Queue
from google.appengine.api.urlfetch import Fetch
from nebhs.models import Animal, AnimalPhoto
from ragendja.template import TextResponse

import html5lib
from BeautifulSoup import BeautifulSoup as BS
from html5lib import sanitizer, treebuilders

try:
    from settings import DEBUG
except:
    DEBUG = False

import logging

PETHARBOR_URLS = {
'dogs': """http://petharbor.com/results.asp?searchtype=ADOPT&stylesheet=include/default.css&frontdoor=1&friends=1&samaritans=1&nosuccess=0&rows=500&imght=120&imgres=thumb&view=sysadm.v_animal&fontface=arial&fontsize=10&zip=68101&miles=200&shelterlist=%27NEHS%27&atype=dog&ADDR=undefined&nav=1&start=4&nomax=1&page=1&where=type_DOG""",
'cats': """http://petharbor.com/results.asp?searchtype=ADOPT&stylesheet=include/default.css&frontdoor=1&friends=1&samaritans=1&nosuccess=0&rows=500&imght=120&imgres=thumb&view=sysadm.v_animal&fontface=arial&fontsize=10&zip=68101&miles=200&shelterlist=%27NEHS%27&atype=cat&ADDR=undefined&nav=1&start=4&nomax=1&page=1&where=type_CAT""",
'other':"""http://petharbor.com/results.asp?searchtype=ADOPT&stylesheet=include/default.css&frontdoor=1&friends=1&samaritans=1&nosuccess=0&rows=500&imght=120&imgres=thumb&view=sysadm.v_animal&fontface=arial&fontsize=10&zip=68101&miles=200&shelterlist=%27NEHS%27&atype=other&ADDR=undefined&nav=1&start=4&nomax=1&page=1&where=type_OO"""}


RATE_LIMIT_MSG="""We are very sorry, but due to high usage we were unable to process your request. Please wait a few moments and try again."""

# TODO: randomize zip code
def _get_petharbor_url(category):
    return PETHARBOR_URLS[category]

def _to_json(s,indent=0):
    return json.dumps(s,indent=indent)

def _load_html(path):
    return unicode(''.join(open(path).readlines()),errors='replace')

def parse_time_phrase(s):
    n,unit = map(lambda x: x.strip(), s.split(' '))
    n = int(n)
    if unit.startswith("year"):
        return n
    elif unit.startswith("month"):
        return n / 12.0

def fetch(url, headers={},**kwargs):
    deadline=kwargs.get('deadline',10)
    headers.update({
        'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14'
    })
    page = Fetch(url, headers, deadline=deadline, **kwargs)
    if DEBUG:
        # store the page
        logging.debug(page.content)
    return page

def parse_petharbor_age(s):
    """
    Age Unknown
    1 year, 6 months old
    10 months old
    1 year
    2 years
  	4 years old    
    """
    s = s.strip().lower()

    if s=="age unknown":
        return None #777?

    # strip a trailing 'old'    
    if s.endswith(" old"):
        s = s[:-4]

    # compound    
    if ',' in s:
        return reduce(lambda x,y: x + parse_time_phrase(y), s.split(', '), 0)

    return parse_time_phrase(s)

def parse_cond_parens(s,reverse=False):
    s = s.strip()
    sp = s.split('(',1)
    if len(sp) == 2:
        return sp[0].strip(), sp[1].strip()[:-1]
    if reverse:
        return '', s
    return s, ''

# TODO: wtf
def parse_desc_age(s):
    """
    Return (description, age)
    """
    s = s.strip().lower()
    sp = s.split('shelter staff think')
    if len(sp) == 2:
        age = sp[1].split('is about')[1].split('.')[0]
        return sp[0], float(parse_petharbor_age(age.strip()))
        #"Shelter staff think%s" % sp[1]

    sp = s.split("this animal's age is unknown")
    if len(sp) == 2:
        return sp[0], None

    raise Exception

def capitalize_first(s):
    return ' '.join(map(lambda x: x.capitalize(), s.split(' ')))

def parse_petharbor_table(content,category=None, batch_id=None):

    # cleanup html
    bs = BS(content)

    parser = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer,
        tree=treebuilders.getTreeBuilder("beautifulsoup"))

    # build parse tree
    tree = parser.parse(bs.encode())
    print '======='

    results = tree.findAll("table",attrs={'class':'ResultsTable'})[0]

    ret = []

    for row in results.findAll('tr')[1:]:
        columns = row.findAll('td')
        cells = map(lambda x:x.encodeContents(), columns)
        # Split Name and ID
        name, code = parse_cond_parens(cells[1], reverse=True)
        # Split gender and spayed_or_neutered
        gender,spayed_or_neutered = parse_cond_parens(cells[2])
        ret.append(
            {'petharbor_url': "http://petharbor.com/%s" % columns[0].find('a')['href'],
             'petharbor_img_thumb_url': columns[0].find('img')['src'],
             'name':capitalize_first(name) or code,
             'code':code,
             'gender':gender,
             'spayed_or_neutered':spayed_or_neutered,
             'main_color':cells[3],
             'breed':cells[4],
             'age':parse_petharbor_age(cells[5]),
             'brought_to_shelter':cells[6],
             'located_at':cells[7],
             'category':category,
             'batch_id':batch_id
             })

    return ret

def parse_petharbor_profile(contents):
    code, desc_age = contents.split('ID#')[1].split('Thank you for')[0].split('<BR><BR></font>')
    logging.debug("desc_age: '%s'" % desc_age)
    desc, age = parse_desc_age(desc_age.strip('<BR>'))
    logging.debug("desc, age: '%s','%s'" % (desc,age))
    petharbor_last_updated = contents.split('old and may not represent')[0].split('This information is ')[1].strip()
    petharbor_img_url = "http://petharbor.com/get_image.asp%s" % contents.split('get_image.asp')[1].split('"')[0]
    return {'code':code,
            'description':desc.strip(),
            'age':age,
            'perharbor_last_updated':petharbor_last_updated,
            'petharbor_img_url':petharbor_img_url}


def task_enqueue_categories(request):
    """
    Enqueues animal tables. To be run by cron
    """
    q = Queue('animal-indexes')
    category = None #request.GET.get('category')
    if category:
        taskqueue.add(Task(url='/adopt/_tasks_/fetch_category',method='post',payload=json.dumps({'category':category, 'url':_getpetharbor_url(x)})))
    else:
        for x in PETHARBOR_URLS.keys():
            q.add(Task(url='/adopt/_tasks_/fetch_category',name="fetch-%s-%s" % (x, datetime.datetime.now().strftime('%Y%m%d%H%M%S')), method='post',payload=str(json.dumps({'category':x,'url':_get_petharbor_url(x)}))))
    return TextResponse('OK')

def task_fetch_category(request):
    logging.debug(dir(request))
    logging.debug(request.build_absolute_uri())
    if request.method=="POST":
        params = json.loads(request.raw_post_data)
        _task_fetch_category(params['url'],params['category'])
    return TextResponse('OK')

def _task_fetch_category(url,category):
    """
    Fetch an animal table, parse out information, and enqueue a task to fetch the image and store the data in the database
    """
    q = Queue('animal-profiles')
    page = fetch(url)
    animals = parse_petharbor_table(page.content,category)
    for animal in animals:
        q.add(Task(url='/adopt/_tasks_/fetch_animal',name="fetch-%s-%s" % (category, animal['code']), method="post",payload=str(json.dumps(animal))))
        #print to_json(x,indent=4)


def task_fetch_animal(request):
    if request.method=="POST":
        data = json.loads(request.raw_post_data)
        animal = dict(map(lambda x: (str(x[0]), x[1]), data.items()))
        month,day,year = animal['brought_to_shelter'].split('/')
        animal['brought_to_shelter'] = datetime.date(int(year), int(month), int(day))
        _task_fetch_profile(animal)
    return TextResponse('OK')

def _task_fetch_profile(animal):
    """
    Fetch an animal image
    """
    page = fetch(animal['petharbor_url'])
    profile = parse_petharbor_profile(page.content)
    animal.update(profile)
    img = Fetch(animal['petharbor_img_url'])

    logging.debug(animal)

    # fetch record
    record = db.Query(Animal).filter('code =',animal['code']).filter('brought_to_shelter =', animal['brought_to_shelter']).filter('category =',animal['category']).get()
    # TODO: assuming animal id is actually unique
    #record = Animal.get_or_insert(animal['code'],image=], image_bytes=img.content), **data)

    # If no record exists
    if not record:
        photo=AnimalPhoto.create(animal['petharbor_img_url'], image_bytes=img.content)
        logging.debug("%s: %s" % (type(photo), photo.__class__))
        photo.put()
        record = Animal(photo=photo, status='adoptable', **animal)
        record.put()
    # If there's an existing record
    elif record.photo.image_bytes[:1000] != img.content[:1000]:
        record.image=AnimalPhoto.create(animal['petharbor_img_url'],image_bytes=img.content)
        record.status='adoptable'
        record.put()

#    # TODO: real hash
#    if record.image_bytes[:1000] != img[:1000]:
#        image = AnimalPhoto.create(animal['petharbor_img_url'], image_bytes=img.content)
#        record.image = image
#        image.put()
#        record.put()

import unittest
class TestDogsTask(unittest.TestCase):
    def _testSet(self,path,category,batch_id):
        content = _load_html(path)
        animals = parse_petharbor_table(content,category,batch_id)
        self.assertTrue(isinstance(animals,list))
        return animals 

    def atestParseAllTables(self):
        batch_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        res = {}
        sets = ['dog','cat','oo']
        for k in sets:
            rows = self._testSet('/home/wturner/projects/mis/whatismis/nebhs/tests/%s_list.html' % k, k, batch_id)
            res[k] = rows
            print _to_json(sorted(rows))
        
        total = 0
        for k in sets:
            n = len(res[k])
            print k, n
            total += n
        print ''
        print "Total:", total

    def testParseProfile(self):
        content = _load_html('/home/wturner/projects/mis/whatismis/nebhs/tests/a672988.html')
        res = parse_petharbor_profile(content)
        print _to_json(res)
        

if __name__ == '__main__':
    #print fetch_dogs_table()
    unittest.main()
