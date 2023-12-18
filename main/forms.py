from captcha.fields import CaptchaField
from django import forms


class ContactForm(forms.Form):
        name=forms.CharField(min_length=5, label='Имя Фамилия', required=True,
                             widget=forms.TextInput(attrs={'placeholder':
                                                           'Ваше имя, Фамилия',
                                                           'class': 'form-control'})
                             )
        email=forms.EmailField(label='E-mail', required=True,
                widget=forms.EmailInput(attrs={'placeholder': 'E-mail',
                                               'class': 'form-control'})
                )
        theme=forms.CharField(min_length=10, label='Тема', required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Тема сообщения',
                                                           'class': 'form-control'})
                             )
        message=forms.CharField(label='Сообщение', required=True,
                min_length=15,
                widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                      'class': 'form-control'})
                )
        captcha = CaptchaField( )