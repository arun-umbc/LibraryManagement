from rest_framework import serializers

from library_app.models import Book, User


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'name', 'author')


class BookRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('created_at', 'updated_at')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'department', 'study_level')
