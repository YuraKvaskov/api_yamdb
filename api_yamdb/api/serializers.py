from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator(), ]
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, data):
        """
        Запрещает пользователям регистрироваться под именем 'me'
        и использовать повторные username и email.
        """
        test_username = User.objects.filter(
            username=data['username']).exists()
        test_email = User.objects.filter(
            email__iexact=data['email']).exists()
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя')
        if User.objects.filter(
                username=data['username'],
                email=data['email']).exists():
            return data
        if test_username:
            raise serializers.ValidationError(
                'Этот username уже использовался')
        if test_email:
            raise serializers.ValidationError(
                'Этот email уже использовался')
        return data


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator(), ]
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator(), ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        """
        Запрещает пользователям регистрироваться
        под именем 'me' и использовать
        повторные username и email.
        """
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if User.objects.filter(
                username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с этим username уже существует'
            )
        if User.objects.filter(
                email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с этим email уже существует'
            )
        return data


class GenreSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',)
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Review
        fields = ('id',
                  'text',
                  'author',
                  'score',
                  'pub_date',)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if (
            title.reviews.filter(author=author).exists()
            and self.context.get('request').method != 'PATCH'
        ):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Недопустимое значение!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = ('id',
                  'text',
                  'author',
                  'pub_date',)
