from django.http import HttpResponse
from django.shortcuts import render

def handle_error404(request ,exception):
    return render(request, 'main/message.html', {"message": "Упс, такая страница не найдена"})

def handle_error500(request):
    return render(request, 'main/message.html', {"message": "Упс, такая страница не найдена"})
