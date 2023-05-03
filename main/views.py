from django.shortcuts import render
from django.http import HttpResponse

from main.forms import ContactForm

from django.conf import settings
from django.core.mail import send_mail

from tortuga.settings import EMAIL_RECIPIENT


# Create your views here.
def index(request):
    data={'title': 'Центр временного содержания и реабилитации черепахи Никольского',
          'values':['Some', 'Hello', '123'],
          'obj':{
              'car': 'Toyota',
              'age': 18,
              'hobby': 'Drink'
            }
          }
    #return HttpResponse("<h4>TestFromHere</h4>")
    return render(request, "main/index.html", data)

def about(request):
#    return HttpResponse("<h4>AboutInfo</h4>")
    return render(request, "main/about.html")

def contacts(request):
    error = ''
    dictForm = {'name': '', 'email': '', 'theme': '', 'message': ''}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mailmessage=f"Сообщение с сайта tortuga-center.ru\n" \
                        f"От: {form.cleaned_data['name']}  E-mail: {form.cleaned_data['email']} \n" \
                        f"Тема: {form.cleaned_data['theme']} \n{form.cleaned_data['message']}\n"
            send_mail(form.cleaned_data['theme'],
                      mailmessage,
#                      form.cleaned_data['message'],
                      settings.EMAIL_HOST_USER, [EMAIL_RECIPIENT])
            return render(request, "main/message.html", { 'message': 'Сообщение отправлено' })
#            return HttpResponse("<h4>Отправка сообщения</h4>")
#            {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['theme']} {form.cleaned_data['message']}")
        else:
            dictForm={'name': form.cleaned_data['name'],
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
    #    return HttpResponse("<h4>Contacts</h4>")
    return render(request, "main/contacts.html", data)
