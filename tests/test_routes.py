from http import HTTPStatus

import pytest
from django.urls import reverse

from metrika.models import Metrika


@pytest.mark.parametrize(
    'name',
    ('home', 'about', )
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('forum_home', )
)
def test_pages_availability_for_auth_user(admin_client, name):
    url = reverse(name)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_empty_db():
    notes_count = Metrika.objects.count()
    assert notes_count == 0


def test_metrika_exists(metrika):
    metrika_count = Metrika.objects.count()
    assert metrika_count == 1
    assert metrika.text == 'Текст заметки'
