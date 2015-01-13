from django.test.utils import override_settings
from tinyblog.utils import tinyblog_bleach


def test_notags():
    assert tinyblog_bleach('foobar') == 'foobar'


def test_no_classes():
    assert tinyblog_bleach(
        '<strong class="western">foo</strong>'
    ) == '<strong>foo</strong>'


def test_links_work():
    assert tinyblog_bleach(
        '<a class="cat" href="bar">foo</a>'
    ) == '<a href="bar">foo</a>'


def test_paragraphs_allowed():
    assert tinyblog_bleach(
        '<p class="western">foo</p>'
    ) == '<p>foo</p>'


@override_settings(TINYBLOG_NO_BLEACH=True)
def test_no_bleach_if_disabled():
    assert tinyblog_bleach(
        '<div class="western">bar</div>'
    ) == '<div class="western">bar</div>'


@override_settings(TINYBLOG_NO_BLEACH=False)
def test_bleach_if_enabled():
    assert tinyblog_bleach(
        '<div class="western">bar</div>'
    ) == 'bar'


@override_settings(TINYBLOG_ALLOWED_TAGS=['div', ])
def test_overriding_allowed_tags():
    assert tinyblog_bleach(
        '<div class="western">bar</div>'
    ) == '<div>bar</div>'


@override_settings(TINYBLOG_ALLOWED_ATTRIBUTES={'p': ['class', ]})
def test_overriding_allowed_attributes():
    assert tinyblog_bleach(
        '<p class="western">bar</p>'
    ) == '<p class="western">bar</p>'
