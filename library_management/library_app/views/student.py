from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from library_app.models import Book, User, Request, Reserve
from library_app.serializers.student import BookListSerializer, BookRetrieveSerializer, ProfileSerializer, \
    RequestListSerializer, RequestRetrieveSerializer, RequestWriteSerializer, ReserveRetrieveSerializer, \
    ReserveListSerializer
from utilities.helper import create_response_dict
from utilities.messages import STUDENT_BOOK_FETCH_SUCCESS, STUDENT_BOOK_FETCH_FAIL, STUDENT_BOOK_RETRIEVE_SUCCESS, \
    STUDENT_BOOK_RETRIEVE_FAIL, STUDENT_PROFILE_RETRIEVE_SUCCESS, STUDENT_PROFILE_RETRIEVE_FAIL, \
    STUDENT_REQUEST_FETCH_SUCCESS, STUDENT_REQUEST_FETCH_FAIL, STUDENT_REQUEST_RETRIEVE_SUCCESS, \
    STUDENT_REQUEST_RETRIEVE_FAIL, STUDENT_REQUEST_CREATE_SUCCESS, STUDENT_REQUEST_CREATE_FAIL, \
    STUDENT_REQUEST_DELETE_FAIL, STUDENT_REQUEST_DELETE_SUCCESS, STUDENT_RESERVE_FETCH_SUCCESS, \
    STUDENT_RESERVE_FETCH_FAIL, STUDENT_RESERVE_RETRIEVE_SUCCESS, STUDENT_RESERVE_RETRIEVE_FAIL, \
    STUDENT_FORGOTTEN_SUCCESS, STUDENT_FORGOTTEN_FAIL
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


class RequestViewSet(GenericViewSet):
    queryset = Request.objects.filter().order_by('-created_at')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomOffsetPagination

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return RequestRetrieveSerializer
        elif self.action in ['partial_update', 'create']:
            return RequestWriteSerializer
        return RequestListSerializer

    def list(self, request, *args, **kwargs):
        """
        API to list requests
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = self.get_queryset().filter(user=request.user)
            pagination = request.GET.get('offset', False)
            if pagination:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True, context={'request': request})
                    paginated_data = self.get_paginated_response(serializer.data)
                    data = create_response_dict(paginated_data['data'], STUDENT_REQUEST_FETCH_SUCCESS, True,
                                                page=paginated_data['page'])
                    return Response(data, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_REQUEST_FETCH_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_REQUEST_FETCH_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """
        API to retrieve a request
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_REQUEST_RETRIEVE_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_REQUEST_RETRIEVE_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """
        API to create a request
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = create_response_dict(serializer.data, STUDENT_REQUEST_CREATE_SUCCESS, True)
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = create_response_dict('', STUDENT_REQUEST_CREATE_FAIL, False)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_REQUEST_CREATE_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        API to hard delete request
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                data = create_response_dict([], STUDENT_REQUEST_DELETE_FAIL, False)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            data = create_response_dict([], STUDENT_REQUEST_DELETE_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_REQUEST_DELETE_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReserveViewSet(GenericViewSet):
    queryset = Reserve.objects.filter().order_by('-created_at')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomOffsetPagination

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return ReserveRetrieveSerializer
        return ReserveListSerializer

    def list(self, request, *args, **kwargs):
        """
        API to list reserves
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = self.get_queryset().filter(request__user=request.user)
            pagination = request.GET.get('offset', False)
            if pagination:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True, context={'request': request})
                    paginated_data = self.get_paginated_response(serializer.data)
                    data = create_response_dict(paginated_data['data'], STUDENT_RESERVE_FETCH_SUCCESS, True,
                                                page=paginated_data['page'])
                    return Response(data, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_RESERVE_FETCH_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_RESERVE_FETCH_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """
        API to retrieve a reserve
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, context={'request': request})
            data = create_response_dict(serializer.data, STUDENT_RESERVE_RETRIEVE_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_RESERVE_RETRIEVE_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgottenView(GenericAPIView):
    queryset = User.objects.filter()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomOffsetPagination

    def post(self, request, *args, **kwargs):
        """
        Student forgotten API
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            user = request.user
            user.delete()
            data = create_response_dict([], STUDENT_FORGOTTEN_SUCCESS, True)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = create_response_dict(str(e), STUDENT_FORGOTTEN_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
