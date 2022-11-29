from django.contrib import admin
from .models import User, Projet, SousTache

# Register your models here.

admin.site.register(User)
admin.site.register(Projet)
admin.site.register(SousTache)
