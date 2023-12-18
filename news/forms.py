from django import forms
from django.forms import DateTimeInput, ModelForm, Textarea, TextInput

from .models import ArticlePicture, Articles


class DateInput(forms.DateInput):
    input_type = 'date'


class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = [
            'title',
            'anons',
            'full_detx',
            'date',
            'picture_url',
            'video_url']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс статьи'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
            "full_detx": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст статьи'
            }),
            "picture_url": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ссылка на картинку'
            }),
            "video_url": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ссылка на видео'
            })
        }


class PictureForm(ModelForm):
    class Meta:
        model = ArticlePicture
        fields = ['title', 'picture_url']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание картинки'
            }),
            'picture_url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ссылка на картинку'
            })
        }
