from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from library_app.serializers.common import UserLoginSerializer
from utilities.helper import create_response_dict
from utilities.messages import LOGIN_SUCCESS, LOGIN_INVALID_CREDENTIALS, LOGIN_FAIL


class UserLogin(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        User Login
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                response_data = create_response_dict(serializer.data, LOGIN_SUCCESS, True)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                data = create_response_dict('', LOGIN_INVALID_CREDENTIALS, False)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = create_response_dict(str(e), LOGIN_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
