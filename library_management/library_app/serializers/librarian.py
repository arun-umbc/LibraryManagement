from rest_framework import serializers

from library_app.models import Book, Request
from utilities.constants import REQUEST_STATUS, REQUEST_FOR


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'name', 'author')


class BookRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('created_at', 'updated_at')


class RequestListSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.user_id')
    book_name = serializers.CharField(source='book.name')

    class Meta:
        model = Request
        fields = ('request_id', 'request_for', 'user_id', 'book_name')


class RequestRetrieveSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.user_id')
    book_name = serializers.CharField(source='book.name')
    book_author = serializers.CharField(source='book.author')
    total_copies = serializers.IntegerField(source='book.total_copies')
    copies_available_rent = serializers.IntegerField(source='book.copies_available_rent')
    copies_available_sale = serializers.IntegerField(source='book.copies_available_sale')
    fine = serializers.FloatField(source='book.fine')
    price = serializers.FloatField(source='book.price')

    class Meta:
        model = Request
        fields = ('request_id', 'request_for', 'user_id', 'book_name', 'book_author', 'total_copies',
                  'copies_available_rent', 'copies_available_sale', 'fine', 'price')


class RequestUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        request_status = validated_data['request_status']
        if request_status == REQUEST_STATUS.approved:
            request_for = instance.request_for
            if request_for == REQUEST_FOR.rent:
                copies_available_rent = instance.book.copies_available_rent
                if copies_available_rent > 0:
                    updated_copies = copies_available_rent - 1
                    instance.book.copies_available_rent = updated_copies
                    instance.book.save()
                else:
                    raise serializers.ValidationError('Check book supplies')
            else:
                copies_available_sale = instance.book.copies_available_sale
                if copies_available_sale > 0:
                    updated_copies = copies_available_sale - 1
                    instance.book.copies_available_sale = updated_copies
                    instance.book.save()
                else:
                    raise serializers.ValidationError('Check book supplies')
        instance.request_status = request_status
        instance.save()
        return instance

    class Meta:
        model = Request
        fields = ('request_status', )
