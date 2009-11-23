from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'nebhs/jcarousel/lib/jquery.jcarousel.js',
    'nebhs/jcarousel/lib/thickbox/thickbox.js',
    'nebhs/corner/jquery.corner.src.js',
    'nebhs/jquery.jquote.3.js'
)

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'nebhs/jcarousel/lib/jquery.jcarousel.css',
    'nebhs/jcarousel/skins/ie7/skin.css',
    'nebhs/jcarousel/skins/tango/skin.css',
    'nebhs/jcarousel/skins/nhs_main/skin.css',
    'nebhs/jcarousel/skins/nhs_mini/skin.css',
    'nebhs/jcarousel/lib/thickbox/thickbox.css'
)

DEFAULT_IMAGE_UNAVAILABLE = "/media/images/yea"