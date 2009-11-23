from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'nebhs/jcarousel/lib/jquery.jcarousel.js',
    'nebhs/jcarousel/lib/thickbox/thickbox.js',
    'nebhs/corner/jquery.corner.src.js'
)

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'nebhs/jcarousel/lib/jquery.jcarousel.css',
    'nebhs/jcarousel/skins/ie7/skin.css',
    'nebhs/jcarousel/lib/thickbox/thickbox.css'
)