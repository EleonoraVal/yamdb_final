from django.db.models import Avg

from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerCreate)

from reviews.models import Category, Genre, Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для работы с произведениями (Titles). """
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleSerializerCreate
        return TitleSerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Viewset для работы с жанрами (Genres). """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    """Viewset для работы с категориями(Categories). """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_review(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )
        return review

    def perform_create(self, serializer):
        review = self.get_review()
        return serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        return self.get_review().comments.all()
