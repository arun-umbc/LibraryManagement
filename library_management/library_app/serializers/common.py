from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from library_app.models import User
from utilities.constants import ROLE_TYPES


class SignUpSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        password = validated_data.pop('password')
        validated_data['role'] = ROLE_TYPES.student
        instance = User.objects.create_user(user_id, password, **validated_data)
        return instance

    class Meta:
        model = User
        exclude = ('role', 'request', 'is_active', 'is_staff', 'created_at', 'updated_at')


class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.CharField(read_only=True)
    authentication_token = serializers.CharField(read_only=True)

    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')
        authenticated_user = authenticate(user_id=user_id, password=password)
        if authenticated_user is not None:
            (token, created) = Token.objects.get_or_create(user=authenticated_user)
            authenticated_user.authentication_token = token.key
            update_last_login(None, user=authenticated_user)
            return authenticated_user
        else:
            raise serializers.ValidationError("Invalid Log In credentials")
