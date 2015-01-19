from django.conf import settings
import bleach


DEFAULT_TINYBLOG_ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'strong',
    'ul',
]


DEFAULT_TINYBLOG_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
}


def tinyblog_bleach(content):
    if hasattr(settings, 'TINYBLOG_NO_BLEACH'):
        if settings.TINYBLOG_NO_BLEACH:
            return content

    allowed_tags = DEFAULT_TINYBLOG_ALLOWED_TAGS

    if hasattr(settings, 'TINYBLOG_ALLOWED_TAGS'):
        allowed_tags = settings.TINYBLOG_ALLOWED_TAGS

    allowed_attributes = DEFAULT_TINYBLOG_ALLOWED_ATTRIBUTES

    if hasattr(settings, 'TINYBLOG_ALLOWED_ATTRIBUTES'):
        allowed_attributes = settings.TINYBLOG_ALLOWED_ATTRIBUTES

    return bleach.clean(content,
                        tags=allowed_tags,
                        attributes=allowed_attributes,
                        strip=True)
