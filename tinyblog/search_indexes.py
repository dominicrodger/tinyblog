from haystack.indexes import SearchIndex, CharField
from haystack import site
from tinyblog.models import Post

class PostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def get_updated_field(self):
        return u'created'

    def index_queryset(self):
        return Post.published_objects.all()

site.register(Post, PostIndex)
