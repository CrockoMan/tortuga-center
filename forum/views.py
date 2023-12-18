import os.path
from datetime import datetime
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import register
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import DeleteView

from forum.forms import ChaptersForm, MessageForm, ThemeForm
from forum.models import Chapters, MessageImages, Messages, Themes


# Create your views here.
def get_client_ip(request):
    """Получить IP клиента."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required()
def forum_create_quote_message(request, chapter_id, theme_id, message_id):
    """Ответить с цитированием."""
    theme = get_object_or_404(Messages, pk=message_id)
    return HttpResponse(f"<h4>Ответить с цитированием {id} {theme.theme_id} <br> {request.META}</h4>")


@login_required()
def forum_create_message(request, chapter_id, pk):
    """Создать сообщение."""
    theme = get_object_or_404(Themes, pk=int(pk))

    form = MessageForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ip = get_client_ip(request)
        if form.is_valid():
            image = request.FILES.getlist('image', [])
            theme.date = datetime.now()
            theme.posts = theme.posts + 1
            theme.save()
            message = Messages(theme_id_id=int(pk),
                               chapter_id_id=chapter_id,
                               message=form.cleaned_data['message'],
                               owner=request.user,
                               ip_addr=ip
                               )
            message.save()
            if image:
                for current_image in image:
                    messageimage = MessageImages(message_id_id=message.pk,
                                                 image=current_image)
                    messageimage.save()

            return redirect(reverse('message', args=[chapter_id, pk]))

    return render(request, 'forum/newmessage.html',
                  {'form': form, 'theme': theme})


def forum_message(request, chapter_id, id):
    """Вывод сообщений темы."""
    theme = get_object_or_404(Themes, pk=int(id))
    messages = Messages.objects.filter(theme_id=theme).prefetch_related('picture')

    chapter = get_object_or_404(Chapters, title=theme.chapter_id)
    theme.views = theme.views + 1
    theme.save()
    return render(request, 'forum/message.html', {'message': messages,
                                                  'theme': theme,
                                                  'chapter': chapter,})


class ForumMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Messages
    template_name = 'forum/delete_message.html'

    def get_object(self, queryset=None):
        chapter_id = self.kwargs.get('chapter_id')
        theme_id = self.kwargs.get('theme_id')
        message_id = self.kwargs.get('message_id')
        obj = self.model.objects.get(chapter_id=chapter_id,
                                     theme_id=theme_id,
                                     id=message_id)
        return obj

    def delete(request, *args, **kwargs):
        chapter_id = kwargs.get('chapter_id')
        theme_id = kwargs.get('theme_id')
        message_id = kwargs.get('message_id')
        message = get_object_or_404(Messages, pk=message_id)
        message_images = MessageImages.objects.filter(message_id=message)
        for file in message_images:
            image = f'{settings.MEDIA_ROOT}/{file.image}'
            if os.path.exists(image):
                os.remove(image)
                file.delete()
        message.delete()
        return redirect(reverse('message', args=[chapter_id, theme_id]))


def forum_hide_message(request, chapter_id, theme_id, message_id):
    """Скрыть сообщение."""
    return HttpResponse(f'<h4>Скрать сообщение</h4>')


@login_required()
def forum_create_theme(request, id, themes=None):
    """Создать новую тему."""
    if request.method == 'POST':
        ip = get_client_ip(request)
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = Themes(title=form.cleaned_data['title'],
                           chapter_id_id=int(id),
                           owner=request.user,
                           ip_addr=ip,
                           posts=1
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
            base_url = reverse('message', args=(themeid,))
            query_string = urlencode({'id': themeid})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        form = ThemeForm()
    return render(request, 'forum/newtheme.html', {'form': form})


def forum_themes(request, id):
    """Список тем."""
    chapter = get_object_or_404(Chapters, pk=int(id))
    themes_list = chapter.themes.all().order_by('-date')
    return render(request, "forum/themes.html", {'themes': themes_list,
                                                 'chapter': chapter})


def forum_home(request):
    """Список разделов форума."""
    chapters_list = Chapters.objects.all().order_by('id')
    return render(request, "forum/forum_main.html",
                  {'chapters': chapters_list})


@login_required()
def forum_create_chapter(request):
    """Создать раздел форума."""
    if request.method == 'POST':
        form = ChaptersForm(request.POST)
        if form.is_valid():
            chapter = Chapters(title=form.cleaned_data['title'],
                               position=form.cleaned_data['position'], )
            chapter.save()
            return redirect('forum_home')
    else:
        chapters_list = Chapters.objects.all().order_by('-position')
        form = ChaptersForm(
            initial={
                'position': chapters_list[0].position + 10})
    return render(request, 'forum/newchapter.html', {'form': form})
