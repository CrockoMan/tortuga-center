from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import GenericIPAddressField


# Create your models here.
class Chapters(models.Model):
    title = models.CharField('Название', max_length=150)
    date = models.DateTimeField('Дата', default=datetime.now)
    position = models.IntegerField('Позиция', default=0)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/forum/{self.id}'

    class Meta:
        verbose_name = "Раздел форума"
        verbose_name_plural = "Разделы форума"
        db_table = "chapters"


class Themes(models.Model):
    chapter_id = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=150)
    date = models.DateTimeField('Дата', default=datetime.now)
#    author = models.CharField('Автор', max_length=9)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_addr = GenericIPAddressField(blank=True, null = True)
    is_show = models.BooleanField(default=True)
    views = models.IntegerField('Просмотры', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/forum/{self.chapter_id}/{self.id}'

    class Meta:
        verbose_name = "Темы"
        verbose_name_plural = "Тема"
        db_table = "themes"


class Messages(models.Model):
    theme_id = models.ForeignKey(Themes, on_delete=models.CASCADE)
    chapter_id = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    message = models.TextField('Сообщение')
    date = models.DateTimeField('Дата', default=datetime.now)
#    author = models.CharField('Автор', max_length=9)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    ip_addr = GenericIPAddressField(blank=True, null = True)
    is_show = models.BooleanField(default=True)
    quote_post_id = models.IntegerField('Цитирует пост N', default=0)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return f'/forum/{self.chapter_id}/{self.theme_id}/{self.id}'

    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщение"
        db_table = "messages"
