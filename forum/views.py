from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from forum.forms import ChaptersForm, ThemeForm, MessageForm
from forum.models import Chapters, Themes, Messages

from urllib.parse import urlencode

from datetime import datetime


# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def forum_create_message(request, pk):
    theme = Themes.objects.get(pk=int(pk))
    # ---------------------
    if request.method == 'POST':
        ip = get_client_ip(request)
        form = MessageForm(request.POST)
        if form.is_valid():
            theme = Themes.objects.get(pk=int(pk))
            theme.date = datetime.now()
            theme.save()
            chapter = Chapters.objects.get(title=theme.chapter_id)
            message = Messages(theme_id_id=int(pk),
                               chapter_id_id=chapter.pk,
                               message=form.cleaned_data['message'],
                               owner=request.user,
                               ip_addr=ip
                               )
            message.save()
            #            return HttpResponse(f"<h4>Новый раздел {theme.title} {theme.owner} {theme.ip_addr}</h4>")
            messages = Messages.objects.filter(theme_id=theme.pk)

            base_url = reverse('message', kwargs={'id': int(pk)})
            query_string = urlencode({'chapter': chapter.pk, 'theme': int(pk)})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    #            return render(request, 'forum/message.html', {'message': messages,
    #                                                  'theme': theme,
    #                                                  'chapter': chapter} )
    #            return redirect(message, int(pk) )
    else:
        form = MessageForm()
    # ---------------------
    return render(request, 'forum/newmessage.html', {'form': form, 'theme': theme})


#    return HttpResponse(f'<h4>Создать комментарий темы pk="{theme.pk}"'
#                        f' title="{theme.title}"</h4>')


def forum_message(request, id):
    #    article = Articles.objects.get(title=picture.article_id)
    theme = Themes.objects.get(pk=int(id))
    messages = Messages.objects.filter(theme_id=theme.pk)
    chapter = Chapters.objects.get(title=theme.chapter_id)
    #    return HttpResponse(f'<h4>Сообщения темы theme={theme} messages="{messages}"</h4>')
    return render(request, 'forum/message.html', {'message': messages,
                                                  'theme': theme,
                                                  'chapter': chapter})


def forum_create_theme(request, id, themes=None):
    if request.method == 'POST':
        ip = get_client_ip(request)
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = Themes(title=form.cleaned_data['title'],
                           chapter_id_id=int(id),
                           owner=request.user,
                           ip_addr=ip
                           )
            theme.save()
            themeid = theme.pk
            message = Messages(theme_id_id=themeid,
                               chapter_id_id=int(id),
                               message=form.cleaned_data['message'],
                               owner=request.user,
                               ip_addr=ip
                               )
            message.save()
            #            return HttpResponse(f"<h4>Новый раздел {theme.title} {theme.owner} {theme.ip_addr}</h4>")
            #            return redirect(forum_home)
            base_url = reverse('message', args=(themeid,))
            query_string = urlencode({'id': themeid})
            url = '{}?{}'.format(base_url, query_string)
            #            return HttpResponse(f"<h4>{url}</h4>")
            return redirect(url)
    else:
        form = ThemeForm()
    #    return HttpResponse(f"<h4>Добавить картинку к посту{id}</h4>")
    return render(request, 'forum/newtheme.html', {'form': form})


#    return HttpResponse("<h4>Создать раздел форума</h4>")


def forum_themes(request, id):
    chapter = Chapters.objects.get(pk=int(id))
    themes_list = Themes.objects.filter(chapter_id=int(id)).order_by('-date')
    #    return HttpResponse(f"<h4>Chapter id {chapter.title}</h4>")
    return render(request, "forum/themes.html", {'themes': themes_list,
                                                 'chapter': chapter})


def forum_home(request):
    chapters_list = Chapters.objects.all().order_by('id')
    #    return HttpResponse("<h4>Forum Home</h4>")
    return render(request, "forum/forum_main.html", {'chapters': chapters_list})


def forum_create_chapter(request):
    if request.method == 'POST':
        form = ChaptersForm(request.POST)
        if form.is_valid():
            chapter = Chapters(title=form.cleaned_data['title'],
                               position=form.cleaned_data['position'], )
            chapter.save()
            #            return HttpResponse(f"<h4>Новый раздел {form.cleaned_data['title']}</h4>")
            return redirect('forum_home')
    else:
        form = ChaptersForm()
    #    return HttpResponse(f"<h4>Добавить картинку к посту{id}</h4>")
    return render(request, 'forum/newchapter.html', {'form': form})
#    return HttpResponse("<h4>Создать раздел форума</h4>")
