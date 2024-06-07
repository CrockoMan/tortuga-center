from http import HTTPStatus

import pytest
from django.urls import reverse

from metrika.models import Metrika


@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('home', 'about', )
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
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
    # В пустой БД никаких заметок не будет:
    assert notes_count == 0


def test_metrika_exists(metrika):
    metrika_count = Metrika.objects.count()
    # Общее количество заметок в БД равно 1.
    assert metrika_count == 1
    # Текст объекта, полученного при помощи фикстуры metrika,
    # совпадает с тем, что указан в фикстуре.
    assert metrika.text == 'Текст заметки'
