from django.contrib import admin
from django.db.models import Avg

from reviews.models import Title, Genre, Category, Review, Comment, GenreTitle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name', 'year', 'category')

    def get_genre(self, object):
        """Получаем жанр(ы) произведений."""
        return '\n'.join((genre.name for genre in object.genre.all()))

    get_genre.short_description = 'Жанр/ы произведения'

    def count_reviews(self, object):
        """Вычисляем количество отзывовю"""
        return object.reviews.count()

    count_reviews.short_description = 'Количество отзывов'

    def get_rating(self, object):
        """Расчет рейтинга."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        return round(rating.get('average_score'), 1)

    get_rating.short_description = 'Рейтинг'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('genre',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'pub_date')
    search_fields = ('author',)
