from django.urls import path, include
from forum import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('create_chapter', views.forum_create_chapter, name='forum_create_chapter'),
    path('create_theme/<int:id>', views.forum_create_theme, name='forum_create_theme'),
    path('<int:id>', views.forum_themes, name='themes'),
    path('theme/<int:id>', views.forum_message, name='message'),
    path('add/<int:pk>', views.forum_create_message, name='forum_create_message'),
]
