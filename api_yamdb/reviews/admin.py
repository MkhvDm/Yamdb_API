from django.contrib import admin

from .models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('text', 'author__username',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'review',
        'text',
        'pub_date',
    )
    search_fields = ('text', 'author__username', )
