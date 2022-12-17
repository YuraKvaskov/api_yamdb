from django.db.models import Avg
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.Serializers import GenreSerializer, CategorySerializer, TitleReadSerializer, TitleWriteSerializer
from api.filters import TitleFilter
from reviews.models import Genre, Category, Title


class MyCustomViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pass


class GenreViewSet(MyCustomViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class CategoryViewSet(MyCustomViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

