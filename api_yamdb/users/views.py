from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import EmailSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def action_me(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            role = request.user.role
            serializer.save(role=role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class APIToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token})


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )

        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Код для регистрации.',
            f'Код: {confirmation_code}.',
            settings.DEFAULT_FROM_EMAIL,
            [serializer.data['email']],
        )
        resp = {'email': email, 'username': username}
        return Response(resp, status=status.HTTP_200_OK)
