from django.contrib import admin
from .models import Publisher, ComicTitle, UserProfile


# Register your models here.
class ComicTitleAdmin(admin.ModelAdmin):
    list_display = ('comic_title','publisher','reservations')
    list_filter = ['publisher']
    search_fields = ['comic_title']

admin.site.register(Publisher)
admin.site.register(UserProfile)
admin.site.register(ComicTitle, ComicTitleAdmin)
