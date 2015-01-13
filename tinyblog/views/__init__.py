from datetime import datetime
from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import (
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
)
from tinyblog.models import Post


def post(request, year, month, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month,
                             slug=slug)

    if post.created > datetime.now():
        if not request.user.is_staff:
            raise Http404

    return render_to_response('tinyblog/post.html',
                              {'post': post},
                              context_instance=RequestContext(request))


class TinyBlogIndexView(ArchiveIndexView):
    date_field = 'created'

    def get_queryset(self):
        return Post.published_objects.all()


class TinyBlogYearView(YearArchiveView):
    date_field = 'created'
    make_object_list = True

    def get_queryset(self):
        return Post.published_objects.all()


class TinyBlogMonthView(MonthArchiveView):
    date_field = 'created'
    month_format = '%m'

    def get_queryset(self):
        return Post.published_objects.all()


def jsonify(request):
    data = serializers.serialize("json", Post.published_objects.all())
    return HttpResponse(data)
