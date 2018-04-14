from django.contrib import admin

from .models import Forum, Thread, Comment, Attachment, Tag

# Register your models here.

admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Attachment)
