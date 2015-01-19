# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.auth.models import User
import pytest


@pytest.fixture()
def user():
    theuser = User.objects.create_user('bob', '', 'secret')
    theuser.email = 'bob@example.com'
    theuser.is_staff = True

    theuser.save()
    return theuser
