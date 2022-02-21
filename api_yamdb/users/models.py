from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (USER, 'пользователь'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'администратор')
)


class User(AbstractUser):
    role = models.CharField(
        verbose_name='статус',
        max_length=50,
        choices=CHOICES,
        default=USER,
        help_text='Группа, к которой принадлежит пользователь.',
    )
    bio = models.CharField(
        verbose_name='о пользователе',
        max_length=200,
        blank=True,
        null=True,
        help_text='Описание пользователя.',
    )
    username = models.CharField(
        verbose_name='username',
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text='Имя пользователя на сайте.',
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True,
        help_text='Email.',
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('email',)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self):
        return self.email
