from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create', views.create, name='create'),
    path('create_vk', views.create_vk, name='create_vk'),
    path('<int:key>', views.NewsDetailView_New, name='news-detail'),
    path(
        '<int:pk>/update',
        views.NewsUpdateView.as_view(),
        name='news-update'
    ),
    path(
        '<int:pk>/delete',
        views.NewsDeleteView.as_view(),
        name='news-delete'
    ),
    path('<id>/vk', views.NewsLoadVk, name='newsloadvk'),
    path('profile', views.profile_view, name='profile'),
    path(
        '<int:id>/del_url_pic',
        views.PictureUrlDelete,
        name='picture-url-delete'
    ),
    path(
        '<int:id>/upd_url_pic',
        views.PictureUrlUpdate,
        name='picture-url-update'
    ),
    path(
        '<int:id>/cre_url_pic',
        views.PictureUrlCreate,
        name='picture-url-create'
    ),
]
