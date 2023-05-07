from django.contrib import admin

from forum.models import Chapters, Themes, Messages

# Register your models here.
admin.site.register(Chapters)
admin.site.register(Themes)
admin.site.register(Messages)