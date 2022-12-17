from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import GenreViewSet, CategoryViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]