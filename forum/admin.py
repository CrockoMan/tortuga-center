from django.contrib import admin

from forum.models import Chapters, Themes, Messages, MessageImages

# Register your models here.
admin.site.register(Chapters)
admin.site.register(Themes)
admin.site.register(Messages)
admin.site.register(MessageImages)