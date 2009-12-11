"""
Courtesy of:
    http://lethain.com/entry/2007/dec/12/two-faced-django-part-six-pyfacebook/
    http://www.djangosnippets.org/snippets/1518/
"""
from django import template
from django.conf import settings
from django.template.defaulttags import URLNode, url
from django.contrib.sites.models import Site
from urllib2 import urlparse

register = template.Library()
@register.tag(name='fburl')
def fburl(parser, token):
    try:
        tag_name,  url = token.split_contents()
        return FormatFacebookURL(url)
    except ValueError:
        raise template.TemplateSyntaxError, "Improper number of arguments."
class FormatFacebookURL(template.Node):
    def __init__(self, url):
        self.app_name = getattr(settings, "FACEBOOK_APP_NAME", "appname")
        self.url = url.strip("\"\'")
        
    def render(self, context):
        if settings.PRODUCTION:
            return "http://apps.facebook.com/%s%s" % (self.app_name,
                self.url.replace('/adopt/facebook',''))
        return "%s" % (self.url)


class FBAbsoluteURLNode(URLNode):
    def render(self, context):
        path = super(FBAbsoluteURLNode, self).render(context)

        if settings.PRODUCTION:
            return "http://apps.facebook.com/%s%s" % ( 
                getattr(settings, "FACEBOOK_APP_NAME", "appname"),
                path.replace('/adopt/facebook',''))
        return "%s" % path

@register.tag(name='fbabsurl')
def fbabsurl(parser, token, node_cls=FBAbsoluteURLNode):
    """Just like {% url %} but ads the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar)

class AbsoluteURLNode(URLNode):
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        domain = "http://%s" % Site.objects.get_current().domain
        return urlparse.urljoin(domain, path)

@register.tag(name='absurl')
def absurl(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but ads the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar)

