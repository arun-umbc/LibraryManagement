from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from library_app.models import Book, User
from library_app.serializers.student import BookListSerializer, BookRetrieveSerializer, ProfileSerializer
from utilities.helper import create_response_dict
from utilities.messages import STUDENT_BOOK_FETCH_SUCCESS, STUDENT_BOOK_FETCH_FAIL, STUDENT_BOOK_RETRIEVE_SUCCESS, \
    STUDENT_BOOK_RETRIEVE_FAIL, STUDENT_PROFILE_RETRIEVE_SUCCESS, STUDENT_PROFILE_RETRIEVE_FAIL
from utilities.pagination import CustomOffsetPagination
from utilities.permissions import IsStudent


class BookViewSet(GenericViewSet):
    queryset = Book.objects.filter().order_by('name')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomOffsetPagination

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return BookRetrieveSerializer
        return BookListSerializer

    def list(self, request, *args, **kwargs):
        """
        API to list Books
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = self.get_queryset()
            search = request.GET.get('search', '').lower()
            pagination = request.GET.get('offset', False)
            query = Q()

            if search:
                query.add(Q(name__contains=search), Q.AND)
            if pagination:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True, context={'request': request})
                    paginated_data = self.get_paginated_response(serializer.data)
                    data = create_response_dict(paginated_data['data'], STUDENT_BOOK_FETCH_SUCCESS, True,
                                                page=paginated_data['page'])
                    return Response(data, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_BOOK_FETCH_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_BOOK_FETCH_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """
        API to retrieve a Book
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_BOOK_RETRIEVE_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_BOOK_RETRIEVE_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(GenericAPIView):
    queryset = User.objects.filter()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomOffsetPagination
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        """
        API to retrieve profile of a Student
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            instance = request.user
            serializer = self.get_serializer(instance, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_PROFILE_RETRIEVE_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_PROFILE_RETRIEVE_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
