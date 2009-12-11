# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('nebhs.views',
                       (r'^create_admin_user/$', 'create_admin_user'),
                       url(r'^photos/(?P<image_key>.*)-(?P<width>.*)x(?P<height>.*)\.(?P<extension>.*)$',
                       'serve_image',
                       name='image_serve_scaled'),
                       url(r'^photos/(?P<image_key>.*)\.(?P<extension>.*)$',
                       'serve_image',
                       name='image_serve'
                       ),
                       url(r'^facebook/$', 'facebook_canvas', name='facebook-canvas'),
                       url(r'^facebook/(?P<category>[dogs|cats|other]+)/$', 'facebook_list_animals', name='facebook-list-animals'),
                       url(r'^facebook/(?P<category>[dogs|cats|other]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<name>[\w\+-]+)$', 'facebook_show_animal_by_name', name='fb-show-animal-by-name'),
                       (r'^(?P<category>[dogs|cats|other]+)/$', 'list_animals'),
                       (r'^(?P<category>[dogs|cats|other]+)/(?P<id>A\d+)$', 'show_animal_by_id'),
                       (r'^(?P<category>[dogs|cats|other]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<name>[\w\+-]+)$', 'show_animal_by_name'),
                       #(r'^create/$', 'add_animal'),
                       #(r'^show/(?P<key>.+)$', 'show_animal'),
                       #(r'^edit/(?P<key>.+)$', 'edit_animal'),
                       #(r'^delete/(?P<key>.+)$', 'delete_animal'),
                       #(r'^download/(?P<key>.+)/(?P<name>.+)$', 'download_file'),
                       ) + patterns('nebhs.tasks',
            (r'^_tasks_/enqueue_categories$', 'task_enqueue_categories'),
            (r'^_tasks_/fetch_category$', 'task_fetch_category'),
            (r'^_tasks_/fetch_animal$', 'task_fetch_animal')
    )