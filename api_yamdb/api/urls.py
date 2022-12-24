from rest_framework.routers import DefaultRouter
from django.urls import include, path


from api.views import (GenreViewSet,
                       CategoryViewSet,
                       TitleViewSet,
                       CommentViewSet,
                       ReviewViewSet,
                       UserViewSet,
                       UserReceiveTokenViewSet,
                       UserCreateViewSet)
app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users',
                   UserViewSet)
v1_router.register('genres',
                   GenreViewSet,
                   basename='genres')
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
urlpatterns = [
    path('v1/auth/token/',
         UserReceiveTokenViewSet.as_view({'post': 'create'}),
         name='token'),
    path('v1/auth/signup/',
         UserCreateViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('v1/', include(v1_router.urls)),
]
