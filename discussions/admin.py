from django.contrib import admin

from .models import User, Discussion, Comment

admin.site.register(User)
admin.site.register(Discussion)
admin.site.register(Comment)
