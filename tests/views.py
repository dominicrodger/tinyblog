from django.http import HttpResponseNotFound


def test_404(request):
    return HttpResponseNotFound("Not found")
