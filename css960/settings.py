from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'css960/reset.css',
    'css960/text.css',
#    'css960/forms.css',
    'css960/960.css',
    'css960/lang-%(LANGUAGE_DIR)s.css',
)
settings.add_app_media('combined-print-%(LANGUAGE_DIR)s.css',
    'css960/print.css',
)
#settings.add_app_media('ie.css',
#    'css960/ie.css',
#)
