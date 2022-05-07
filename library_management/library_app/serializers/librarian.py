from datetime import datetime, timedelta

from rest_framework import serializers

from library_app.models import Book, Request, Reserve
from utilities.constants import REQUEST_STATUS, REQUEST_FOR, RETURN_RANGE, RESERVE_STATUS
from utilities.helper import create_db_id


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'name', 'author')


class BookRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('created_at', 'updated_at')


class BookWriteSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        book = Book()
        book.book_id = create_db_id()
        for key, value in validated_data.items():
            setattr(book, key, value)
        book.save()
        return book

    class Meta:
        model = Book
        exclude = ('book_id', 'created_at', 'updated_at')


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
        is_rented = True
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
                is_rented = False
                copies_available_sale = instance.book.copies_available_sale
                if copies_available_sale > 0:
                    updated_copies = copies_available_sale - 1
                    instance.book.copies_available_sale = updated_copies
                    instance.book.save()
                else:
                    raise serializers.ValidationError('Check book supplies')
            reserve = Reserve()
            reserve.reserve_id = create_db_id()
            reserve.request = instance
            if is_rented:
                reserve.rented_date = datetime.utcnow()
                reserve.return_date = reserve.rented_date + timedelta(days=RETURN_RANGE)
                reserve.reserve_status = RESERVE_STATUS.open
            else:
                reserve.purchase_date = datetime.utcnow()
                reserve.reserve_status = RESERVE_STATUS.close
            reserve.save()
        instance.request_status = request_status
        instance.save()
        return instance

    class Meta:
        model = Request
        fields = ('request_status', )


class ReserveListSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source='request.user.user_id')

    class Meta:
        model = Reserve
        fields = ('reserve_id', 'reserve_status', 'student')


class ReserveRetrieveSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='request.book.name')
    student = serializers.CharField(source='request.user.user_id')
    request_for = serializers.CharField(source='request.request_for')

    class Meta:
        model = Reserve
        exclude = ('created_at', 'updated_at', 'request')
