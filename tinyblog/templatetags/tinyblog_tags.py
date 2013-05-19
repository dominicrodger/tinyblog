from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('tinyblog/_post_date.html')
def tinyblog_post_date(object_date):
    return {'thedate': object_date}


@register.assignment_tag
def tinyblog_disqus_shortname():
    if hasattr(settings, 'TINYBLOG_DISQUS_SHORTNAME'):
        return settings.TINYBLOG_DISQUS_SHORTNAME

    return None
