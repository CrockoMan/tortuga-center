from django.urls import path

from forum import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('create_chapter',
         views.forum_create_chapter,
         name='forum_create_chapter'
         ),
    path('chapter/<int:id>/create_theme',
         views.forum_create_theme,
         name='forum_create_theme'),
    path('chapter/<int:id>', views.forum_themes, name='themes'),
    path('chapter/<int:chapter_id>/theme/<int:id>',
         views.forum_message,
         name='message'
         ),
    # path('add/<int:pk>',
    path('chapter/<int:chapter_id>/theme/<int:pk>/add_comment',
         views.forum_create_message,
         name='forum_create_message'
         ),
    path('chapter/<int:chapter_id>/theme/<int:theme_id>/message/<int:message_id>/add_with_quote',
         views.forum_create_quote_message,
         name='forum_create_quote_message'
         ),
    path(
        'chapter/<int:chapter_id>/theme/<int:theme_id>/message/<int:message_id>/delete',
        views.ForumMessageDeleteView.as_view(),
        # views.forum_delete_message,
        name='forum_delete_message'
        ),
    path(
        'chapter/<int:chapter_id>/theme/<int:theme_id>/message/<int:message_id>/hide',
        views.forum_hide_message,
        name='forum_hide_message'
    ),
]
