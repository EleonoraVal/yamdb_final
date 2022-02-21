from django.urls import include, path
from rest_framework import routers
from users.views import APISignup, APIToken, UserViewSet

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api-review',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api-comment'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='user',
)


urlpatterns = [
    path('v1/', include(router_v1.urls), name='api_v1'),
    path('v1/auth/token/', APIToken.as_view(), name='token_api_v1'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup_api_v1'),
]
