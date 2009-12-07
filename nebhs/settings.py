from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'nebhs/js/jcarousel/lib/jquery.jcarousel.js',
    'nebhs/js/jcarousel/lib/thickbox/thickbox.js',
    'nebhs/js/corner/jquery.corner.src.js',
    'nebhs/js/jquery.jquote.3.js',
    'nebhs/js/jquery.metadata.js',
    'nebhs/js/jquery.defaultvalue.source.js',
    'nebhs/js/jquery.twitter.js/jquery.twitter.js'
)

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',

    # Current Convio CSS
#    'nebhs/css/themes/default.css',
#    'nebhs/css/themes/alphacube.css',
#    #'nebhs/css/UserGlobalStyle.css',
#    'nebhs/css/CustomStyle.css',
#    'nebhs/css/CustomWysiwygStyle.css',
    'nebhs/css/look.css',
    'nebhs/js/jcarousel/lib/jquery.jcarousel.css',
    'nebhs/js/jcarousel/skins/ie7/skin.css',
    'nebhs/js/jcarousel/skins/tango/skin.css',
    'nebhs/js/jcarousel/skins/nhs_main/skin.css',
    'nebhs/js/jcarousel/skins/nhs_mini/skin.css',
    'nebhs/js/jcarousel/skins/nhs_adoptions/skin.css',
    'nebhs/js/jcarousel/lib/thickbox/thickbox.css',
    'nebhs/js/jquery.twitter.js/jquery.twitter.css'
)

# TODO
# DEFAULT_IMAGE_UNAVAILABLE = "/media/images/yea"