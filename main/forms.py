from captcha.fields import CaptchaField
from django import forms


NAME_MIN_LEN = 5
THEME_MIN_LEN = 10
MESSAGE_MIN_LEN = 15

class ContactForm(forms.Form):
        name=forms.CharField(
            min_length=NAME_MIN_LEN,
            label='Имя Фамилия',
            required=True,
            widget=forms.TextInput(attrs={'placeholder':
                                              'Ваше имя, Фамилия',
                                          'class': 'form-control'}
                                   )
        )
        email=forms.EmailField(
            label='E-mail',
            required=True,
            widget=forms.EmailInput(attrs={'placeholder': 'E-mail',
                                           'class': 'form-control'}
                                    )
        )
        theme=forms.CharField(
            min_length=THEME_MIN_LEN,
            label='Тема',
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Тема сообщения',
                                          'class': 'form-control'}
                                   )
        )
        message=forms.CharField(
            label='Сообщение',
            required=True,
            min_length=MESSAGE_MIN_LEN,
            widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                         'class': 'form-control'}
                                  )
        )
        captcha = CaptchaField()
