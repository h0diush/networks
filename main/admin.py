from django.contrib import admin

from main.models import Comment, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'rating',
        'author',
        'pub_date',
        'image',
    )
    search_fields = ('title',)
    list_filter = ('pub_date',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
