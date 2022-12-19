from django.contrib import admin

from reviews.models import Title, Genre, Category, Review, Comment
from users.models import User

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
