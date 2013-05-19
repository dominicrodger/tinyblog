from datetime import datetime
from tinyblog.models import Post, EmailSubscriber
import factory


class PostFactory(factory.Factory):
    FACTORY_FOR = Post

    title = factory.Sequence(lambda n: 'Post %s' % n)
    slug = factory.Sequence(lambda n: 'post-%s' % n)
    created = datetime(2013, 1, 1, 7, 0, 0)


class EmailSubscriberFactory(factory.Factory):
    FACTORY_FOR = EmailSubscriber

    email = 'to@example.com'
