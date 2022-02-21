from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'role',
        'username',
        'email',
        'bio',
    )

    list_editable = ('role',)
    search_fields = ('username', 'email')
    list_filter = ('username', 'role')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'score', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author', 'title', 'pub_date')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'review', 'author', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('author', 'review')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'year', 'genre', 'category')
    list_filter = ('name', 'year', 'genre', 'category')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
