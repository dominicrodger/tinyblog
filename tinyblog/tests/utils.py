from datetime import datetime
from tinyblog.models import Post
import factory


class PostFactory(factory.Factory):
    FACTORY_FOR = Post

    title = factory.Sequence(lambda n: 'Post %s' % n)
    slug = factory.Sequence(lambda n: 'post-%s' % n)
    created = datetime(2013, 1, 1, 7, 0, 0)
