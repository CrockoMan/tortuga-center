from http import HTTPStatus

import pytest
from django.urls import reverse

from metrika.models import Metrika

from django.urls import reverse

# В тесте используем фикстуру заметки
# и фикстуру клиента с автором заметки.
def test_note_in_list_for_author(note, author_client):
    url = reverse('notes:list')
    # Запрашиваем страницу со списком заметок:
    response = author_client.get(url)
    # Получаем список объектов из контекста:
    object_list = response.context['object_list']
    # Проверяем, что заметка находится в этом списке:
    assert note in object_list
