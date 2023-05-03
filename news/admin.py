from django.contrib import admin

# Register your models here.
from .models import Articles, ArticlePicture

admin.site.register(Articles)
admin.site.register(ArticlePicture)
