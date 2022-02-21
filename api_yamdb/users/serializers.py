from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'role',
            'bio',
            'email',
        )
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )]

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationaError(
                'This username is impossible to be used.'
            )
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=250,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=250,
        required=True
    )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать такое имя пользователя.'
            )
        return value
