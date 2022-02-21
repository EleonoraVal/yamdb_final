from django.utils import timezone

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами (Genres). """

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями(Categories). """

    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями (Titles). """
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id',)

    def validate_year(self, value):
        year = timezone.now().year
        if not value <= year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями (Titles). """
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    def validate(self, data, *args, **kwargs):
        if self.context['request'].method == 'POST':
            title_id = int(
                self.context['request']
                .parser_context.get('kwargs')
                .get('title_id')
            )
            title = get_object_or_404(Title, pk=title_id)
            if title.reviews.filter(
                author=self.context['request'].user
            ).exists():
                pass
                raise serializers.ValidationError(
                    'Вы можете оставлять только однин отзыв на произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = (
            'id',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text',
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'id',
            'pub_date',
        )
