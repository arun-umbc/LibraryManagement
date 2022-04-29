from rest_framework import serializers

from library_app.models import Book, User, Request
from utilities.constants import REQUEST_STATUS
from utilities.helper import create_db_id


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


class RequestListSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name')

    class Meta:
        model = Request
        fields = ('request_id', 'request_for', 'request_status', 'book_name')


class RequestRetrieveSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name')
    book_author = serializers.CharField(source='book.author')
    fine = serializers.FloatField(source='book.fine')
    price = serializers.FloatField(source='book.price')

    class Meta:
        model = Request
        fields = ('request_id', 'request_for', 'request_status',  'book_name', 'book_author', 'fine', 'price',
                  'created_at')


class RequestWriteSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        req = self.context.get('request')
        request = Request()
        request.request_id = create_db_id()
        request.user = req.user
        request.book = validated_data['book']
        request.request_status = REQUEST_STATUS.pending
        request.request_for = validated_data['request_for']
        request.save()
        return request

    class Meta:
        model = Request
        fields = ('book', 'request_for')
