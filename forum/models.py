from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import GenericIPAddressField

MAX_LENGTH = 50
TITLE_LEN = 200
POST_DEFAULT = 0


class Chapters(models.Model):
    title = models.CharField('Название', max_length=TITLE_LEN)
    date = models.DateTimeField('Дата', default=datetime.now)
    position = models.IntegerField('Позиция', default=POST_DEFAULT)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.title[:MAX_LENGTH]

    def get_absolute_url(self):
        return f'/forum/{self.id}'

    class Meta:
        verbose_name = "Разделы форума"
        verbose_name_plural = "Раздел форума"
        db_table = "chapters"


class Themes(models.Model):
    chapter_id = models.ForeignKey(Chapters,
                                   on_delete=models.CASCADE,
                                   related_name='themes'
                                   )
    title = models.CharField('Название', max_length=TITLE_LEN)
    date = models.DateTimeField('Дата', default=datetime.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_addr = GenericIPAddressField(blank=True, null=True)
    is_show = models.BooleanField(default=True)
    posts = models.IntegerField('Сообщений', default=POST_DEFAULT)
    views = models.IntegerField('Просмотры', default=POST_DEFAULT)

    def __str__(self):
        return self.title[:MAX_LENGTH]

    def get_absolute_url(self):
        return f'/forum/{self.chapter_id}/{self.id}'

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        db_table = "themes"


class Messages(models.Model):
    theme_id = models.ForeignKey(Themes,
                                 on_delete=models.CASCADE,
                                 related_name='messages'
                                 )
    chapter_id = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    message = models.TextField('Сообщение')
    date = models.DateTimeField('Дата', default=datetime.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_addr = GenericIPAddressField(blank=True, null=True)
    is_show = models.BooleanField(default=True)
    quote_post_id = models.IntegerField('Цитирует пост N', default=POST_DEFAULT)

    def __str__(self):
        return self.message[:MAX_LENGTH]

    def get_absolute_url(self):
        return f'/forum/{self.chapter_id}/{self.theme_id}/{self.id}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        db_table = "messages"


class MessageImages(models.Model):
    message_id = models.ForeignKey(Messages,
                                   on_delete=models.CASCADE,
                                   related_name='picture')
    title = models.CharField(max_length=TITLE_LEN)
    image = models.ImageField('Изображение', upload_to='forum_images/%Y%m%d')

    def __str__(self):
        return self.title[:MAX_LENGTH]

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        db_table = "message_images"
