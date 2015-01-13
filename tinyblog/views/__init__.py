from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
    DetailView,
)
from tinyblog.models import Post


class TinyBlogPostView(DetailView):
    template_name = 'tinyblog/post.html'

    def get_object(self):
        post = get_object_or_404(
            Post,
            created__year=int(self.kwargs['year']),
            created__month=int(self.kwargs['month']),
            slug=self.kwargs['slug']
        )

        if post.created > datetime.now():
            if not self.request.user.is_staff:
                raise Http404
        return post
post = TinyBlogPostView.as_view()


class TinyBlogIndexView(ArchiveIndexView):
    date_field = 'created'

    def get_queryset(self):
        return Post.published_objects.all()
index_view = TinyBlogIndexView.as_view()


class TinyBlogYearView(YearArchiveView):
    date_field = 'created'
    make_object_list = True

    def get_queryset(self):
        return Post.published_objects.all()
year_view = TinyBlogYearView.as_view()


class TinyBlogMonthView(MonthArchiveView):
    date_field = 'created'
    month_format = '%m'

    def get_queryset(self):
        return Post.published_objects.all()
month_view = TinyBlogMonthView.as_view()
