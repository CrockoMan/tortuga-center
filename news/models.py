from datetime import datetime

from django.db import models


class Articles(models.Model):
    title = models.CharField('Название', max_length=100)
    anons = models.CharField('Анонс', blank=True, max_length=250)
    full_detx = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации', default=datetime.now)
#    date = models.DateField('Дата публикации', default=datetime.date.today)
    picture_url = models.CharField(
        'Ссылка на картинку',
        blank=True,
        max_length=500)
    video_url = models.CharField('Ссылка на видео', blank=True, max_length=500)
    picture_vk_owner = models.CharField("VK_id", blank=True, max_length=20)
    picture_vk_post = models.CharField("VK_post", blank=True, max_length=20)
    picture_vk_id = models.CharField(
        "VK_picture_id", blank=True, max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        db_table = "articles"


class ArticlePicture(models.Model):
    article_id = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        related_name='pictures')
    title = models.CharField('Название', max_length=100)
    picture_url = models.CharField(
        'Ссылка на картинку',
        blank=True,
        max_length=500)
    picture_vk_owner = models.CharField("VK_id", blank=True, max_length=20)
    picture_vk_post = models.CharField("VK_post", blank=True, max_length=20)
    picture_vk_id = models.CharField(
        "VK_picture_id", blank=True, max_length=20)
    image = models.ImageField(
        'Изображение',
        blank=True,
        upload_to='news_images/%Y%m%d')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        db_table = "article_picture"
