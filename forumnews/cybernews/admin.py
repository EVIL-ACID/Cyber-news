from django.contrib import admin
from .models import Post, Comment, upVote
from mptt.admin import MPTTModelAdmin

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(upVote)