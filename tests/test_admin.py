# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import Client

import pytest


@pytest.mark.django_db
def test_admin_homepage(rf, user):
    client = Client()
    client.login(username='bob', password='secret')

    response = client.get(reverse("admin:index"))
    assert response.status_code == 200
