from datetime import datetime

import vk_api
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import URLField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaultfilters import register
from django.views.generic import DeleteView, DetailView, UpdateView
from tortuga.settings import VK_OWNER_ID, VK_TOKEN

from .forms import ArticlesForm, PictureForm
from .models import ArticlePicture, Articles


POSTS_PER_PAGE = 5
FIRST_PAGE = 1


@register.filter()
def validate_url(url):
    url_form_field = URLField()
    try:
        url_form_field.clean(url)
    except ValidationError:
        return False
    return True


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'news/profile.html'


def profile_view(request):
    return render(request, 'news/profile.html')


def news_home(request):
    post_list = Articles.objects.all().order_by('-date')
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page', FIRST_PAGE)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(FIRST_PAGE)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'news/news_home.html', {'news': posts})


def NewsDetailView_New(request, key):
    article = Articles.objects.get(pk=int(key))
    picture = article.pictures.all()
    return render(request, 'news/news_detail.html', {'article': article,
                                                     'picture': picture})


def PictureUrlDelete(request, id):
    picture = ArticlePicture.objects.get(pk=int(id))
    article = Articles.objects.get(title=picture.article_id)
    picture.delete()
    return redirect(f"/news/{ article.id }")


def PictureUrlUpdate(request, id):
    picture = ArticlePicture.objects.get(pk=int(id))
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            picture.title = form.cleaned_data['title']
            picture.picture_url = form.cleaned_data['picture_url']
            picture.save()
            return redirect(f"/news/{picture.article_id_id}")
    else:
        form = PictureForm(
            initial={
                'title': picture.title,
                'picture_url': picture.picture_url})
    return render(request, 'news/picture_url_update.html', {'picture': form})


def PictureUrlCreate(request, id):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            picture = ArticlePicture(
                article_id_id=int(id),
                title=form.cleaned_data['title'],
                picture_url=form.cleaned_data['picture_url'])
            picture.save()
            return redirect(f"/news/{id}")
    else:
        form = PictureForm()
    return render(request, 'news/picture_url_add.html', {'picture': form})


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/news_detail_views.html'
    context_object_name = 'article'


class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm


class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/delete.html'


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_home')
        else:
            error = 'Ошибка в заполнении формы'
    form = ArticlesForm()
    data = {'form': form,
            'error': error}
    return render(request, 'news/create.html', data)


@register.filter()
def article_cut(article, len):
    return article[:len]


def create_vk(request):
    wall_posts = load_from_vk()
    return render(request, 'news/create_vk.html', {'news': wall_posts})


def load_from_vk(message_count=20, message_offset=1):
    session = vk_api.VkApi(token=VK_TOKEN)
    vk = session.get_api()
    owner_id = VK_OWNER_ID
    wall_posts = vk.wall.get(
        owner_id=owner_id,
        count=message_count,
        offset=message_offset)
    return wall_posts


def say_title(s, ntype):
    csearch = ".!?)("
    nposfound = 0
    ctitle = s
    ctext = ""
    cret = ""
    if len(s) > 0:
        for i in range(len(s)):
            for j in range(len(csearch)):
                if s[i] == csearch[j]:
                    nposfound = i
            if nposfound > 0 and s[i] == " ":
                ctitle = s[:nposfound + 1].strip()
                ctext = s[nposfound + 2:].strip()
                break
        if ntype == 1:
            cret = ctitle
        else:
            cret = ctext
    return cret


def NewsLoadVk(request, id):
    Articles_Model = Articles()
    ArticlePictures = ArticlePicture()
    cstr = ""

    wall_posts = load_from_vk()
    for post in wall_posts['items']:
        if int(post['id']) == int(id):
            cstr = (
                f"{datetime.isoformat(datetime.fromtimestamp(post['date']))} "
                f"{post['text'].split('.',1)[0]} <br>{post['text']} <br>")
            Articles_Model = Articles(
                date=datetime.fromtimestamp(post['date']),
                title=say_title(post['text'], 1),
                anons="",
                full_detx=say_title(post['text'], 2),
                picture_url="")
            Articles_Model.save()
            pk = Articles_Model.pk
            cstr = 'pk=' + \
                f'{Articles_Model.pk} type={type(Articles_Model.pk)}<br>' + cstr
            cstr = 'id=' + f'{Articles_Model.id}' + "<br>" + cstr
            if "attachments" in post:
                for attachment in post['attachments']:
                    if attachment['type'] == 'photo':
                        cstr += (f"OWNER_ID={attachment['photo']['owner_id']} "
                                 f"ID={attachment['photo']['id']}")
                        cstr = (cstr + '<br><a href="' + attachment[
                            'photo']['sizes'][-1]['url'] + '">' +
                                attachment['photo']['sizes'][-1]['url'] +
                                '</a>')
                        cstr = (cstr + '<br><img src="' + attachment[
                            'photo']['sizes'][-1]['url'] + '" width="200">')
                        width = 0
                        url = ''
                        for size in attachment['photo']['sizes']:
                            if int(size['width']) > width:
                                width = int(size['width'])
                                url = size['url']
                        if Articles_Model.picture_url == "":
                            Articles_Model.picture_url = url

                            Articles_Model.picture_vk_owner = attachment['photo']['owner_id']
                            Articles_Model.picture_vk_post = id
                            Articles_Model.picture_vk_id = attachment['photo']['id']

                            Articles_Model.save()
                        else:
                            ArticlePictures = ArticlePicture(
                                article_id_id=pk,
                                title="",
                                picture_url=url,
                                picture_vk_owner=attachment['photo']['owner_id'],
                                picture_vk_post=id,
                                picture_vk_id=attachment['photo']['id']
                            )
                            ArticlePictures.save()
    cstr += f' {wall_posts}'
    return redirect(f"/news/{ pk }")
