from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, NumberInput

from forum.models import Chapters


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
                'min': 1,
                'max': 99999
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
    title = forms.CharField(min_length=10, max_length=150, label='Тема', required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Тема',
                                                          'class': 'form-control'})
                            )
    message = forms.CharField(label='Сообщение', required=True,
                              min_length=15,
                              widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                                           'class': 'form-control'})
                              )


class MessageForm(forms.Form):
    message = forms.CharField(label='Сообщение', required=True,
                              min_length=15,
                              widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                                           'class': 'form-control'})
                              )
    image = forms.ImageField(label='Прикрепить изображение', required=False)
