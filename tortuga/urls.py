from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('auth/', include('loginsys.urls')),
    path('captcha/', include('captcha.urls')),
    path('forum/', include('forum.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)


handler404 = "tortuga.views.handle_error404"
handler500 = "tortuga.views.handle_error500"
