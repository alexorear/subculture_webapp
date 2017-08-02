from django.contrib import admin
from .models import Publisher, ComicTitle, UserProfile
from django.contrib.auth.models import User

from django import forms

# Register your models here.
class ComicTitleAdmin(admin.ModelAdmin):
    list_display = ('comic_title','publisher','reservations')
    list_filter = ['publisher']
    search_fields = ['comic_title']
    filter_horizontal = ['readers']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['comics',]

admin.site.register(Publisher)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ComicTitle, ComicTitleAdmin)
