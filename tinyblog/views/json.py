from django.core import serializers
from django.http import HttpResponse
from tinyblog.models import Post


def serialized_posts(request):
    data = serializers.serialize("json", Post.published_objects.all())
    return HttpResponse(data)
