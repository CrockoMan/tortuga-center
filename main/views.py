from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from main.forms import ContactForm
from main.utils import check_spam
from tortuga.settings import EMAIL_RECIPIENT


def about(request):
    return render(request, "main/about.html")


def contacts(request):
    error = ''
    dictForm = {'name': '', 'email': '', 'theme': '', 'message': ''}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid() and check_spam(form.cleaned_data['theme'],
                                          form.cleaned_data['message']):
            mailmessage = (f"Сообщение с сайта tortuga-center.ru\n"
                           f"От: {form.cleaned_data['name']}  "
                           f"E-mail: {form.cleaned_data['email']} \n"
                           f"Тема: {form.cleaned_data['theme']} \n"
                           f"{form.cleaned_data['message']}\n"
                           )
            send_mail(form.cleaned_data['theme'],
                      mailmessage,
                      #                      form.cleaned_data['message'],
                      settings.EMAIL_HOST_USER, [EMAIL_RECIPIENT])
            return render(request, "main/message.html",
                          {'message': 'Сообщение отправлено'})
        else:
            dictForm = {'name': form.cleaned_data['name'],
                        'email': form.cleaned_data['email'],
                        'theme': form.cleaned_data['theme'],
                        'message': form.cleaned_data['message']}
            error = 'Ошибка в заполнении формы'

    form = ContactForm(initial={'name': dictForm['name'],
                                'email': dictForm['email'],
                                'theme': dictForm['theme'],
                                'message': dictForm['message']})
    data = {'form': form,
            'error': error}
    return render(request, "main/contacts.html", data)
