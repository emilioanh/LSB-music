from django.contrib import admin
from .models import Song, Profile

admin.site.register(Profile)
admin.site.register(Song)