from django import forms
from django.forms import (DateTimeInput, ModelForm, NumberInput, Textarea,
                          TextInput)

from forum.models import Chapters


MIN_LEN = 15
MAX_LEN = 150
ID_MIN = 1
ID_MAX = 99999


class ChaptersForm(ModelForm):
    class Meta:
        model = Chapters
        fields = ['title', 'position']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название раздела'
            }),
            'position': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID раздела',
                'min': ID_MIN,
                'max': ID_MAX
            }),
        }


class ThemeForm_(ModelForm):
    class Meta:
        model = Chapters
        fields = ['title']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название темы'
            }),
        }


class ThemeForm(forms.Form):
    title = forms.CharField(
        min_length=MIN_LEN,
        max_length=MAX_LEN,
        label='Тема',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Тема',
                'class': 'form-control'}))
    message = forms.CharField(
        label='Сообщение',
        required=True,
        min_length=MIN_LEN,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Сообщение',
                'class': 'form-control'}))


class MessageForm(forms.Form):
    message = forms.CharField(
        label='Сообщение',
        required=True,
        min_length=MIN_LEN,
        widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                     'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Прикрепить изображение',
        required=False,
        widget=forms.FileInput(attrs={'multiple': True}))
