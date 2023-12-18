from django.contrib import admin
from django.utils.html import format_html

from forum.models import Chapters, MessageImages, Messages, Themes

# Register your models here.
admin.site.register(Chapters)
admin.site.register(Themes)
# admin.site.register(Messages)


@admin.register(MessageImages)
class MessageImagesAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'title', 'image_preview')
    search_fields = ('title', )
    admin.site.empty_value_display = 'Не задано'

    @admin.display(description='Изображение',)
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" '
                               '/>'.format(obj.image.url))
        else:
            return format_html('')


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_filter = ('theme_id', 'chapter_id',)
    # list_editable = ('category',)
    search_fields = ('message',)
