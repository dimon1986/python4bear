from django.contrib import admin

# Register your models here.
from .models import Topic, Post, Comment

admin.site.register([Topic])


class PostAdmin(admin.ModelAdmin):
    list_display = ('owner','slug', 'topic', 'title', 'publish', 'status', 'image_img')
    list_filter = ('status', 'date_added', 'publish', 'owner')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)} #первычный называется титлом
    raw_id_fields = ('owner',) #таким образом можно поском добавлять тварцов или просто писать целую цыфру
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'post', 'date_added', 'active')
    list_filter = ('active', 'date_added', 'date_up')
    search_fields = ('owner', 'text')

admin.site.register(Comment, CommentAdmin)

