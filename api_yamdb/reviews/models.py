from django.core import validators
from django.db import models

from .validators import year_validator
from users.models import User


class Category(models.Model):
    """Модель для работы с категориями (Categories). """
    name = models.CharField(
        verbose_name='название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для работы с жанрами (Categories). """
    name = models.CharField(
        verbose_name='жанр',
        max_length=256,
        db_index=True
    )

    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для работы с произведениями (Titles). """
    name = models.CharField(
        verbose_name='название произведение',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='год',
        validators=[year_validator]
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        null=True,
        on_delete=models.SET_NULL,
        blank=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='текст отзыва',
        help_text='Здесь вы можете написать свои мысли по поводу произведения',
    )
    title = models.ForeignKey(
        Title,
        models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        help_text='Произведение к которому относится отзыв',
        db_index=True
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
        help_text='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        validators=[
            validators.MinValueValidator(1, 'Минимальное значение = 1'),
            validators.MaxValueValidator(10, 'Максимальное значение = 10'),
        ],
        help_text='Оценка произведения по шкале от 1 до 10',
        db_index=True,
        default=0
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='duplicate_review'
            ),
        ]

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    text = models.TextField(
        verbose_name='комментарий',
        help_text='Здесь можно поделиться своими мыслями по поводу отзыва',
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='comments',
        verbose_name='автор',
        help_text='Автор комментария',
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
        help_text='Отзыв на который оставлен комментарий',
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
