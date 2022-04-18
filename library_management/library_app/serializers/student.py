from rest_framework import serializers

from library_app.models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'name', 'author')


class BookRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('created_at', 'updated_at')
