from datetime import datetime

import pytest

# Импортируем модель заметки, чтобы создать экземпляр.
from metrika.models import Metrika


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author_admin(django_user_model):
    return django_user_model.objects.create(username='admin')


@pytest.fixture
def user_admin(author_admin, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(author_admin)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def metrika(author_admin, user_admin):
    metrika = Metrika.objects.create(  # Создаём объект заметки.
        mark=1,
        date=datetime.now(),
        gender='M',
        age=0,
        status='П',
        health='Н',
        date_free=None,
        text='Текст заметки',
        hidden=False,
        user=author_admin,
    )
    return metrika
