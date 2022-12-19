from rest_framework.routers import DefaultRouter
from django.urls import include, path


from api.views import (GenreViewSet,
                       CategoryViewSet,
                       TitleViewSet,
                       APIGetToken,
                       APISignup,
                       UsersViewSet,
                       CommentViewSet,
                       ReviewViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet)
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/', include(v1_router.urls)),
]