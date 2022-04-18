from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.authtoken.models import Token


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
