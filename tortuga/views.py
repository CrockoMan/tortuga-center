from django.http import HttpResponse
from django.shortcuts import render

def handle_error404(request ,exception):
#    return HttpResponse(f"<h4>Ошибка 404</h4>")
    return render(request, 'main/message.html', {"message": "Упс, такая страница не найдена"})

def handle_error500(request):
    return render(request, 'main/message.html', {"message": "Упс, такая страница не найдена"})
#    return HttpResponse(f"<h4>Ошибка 500</h4>")