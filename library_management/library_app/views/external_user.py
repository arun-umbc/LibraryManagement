import pandas as pd
from django.db.models import Count
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library_app.models import Request
from utilities.helper import create_response_dict, create_df_csv
from utilities.messages import EXTERNAL_USER_DATA_FETCH_SUCCESS, EXTERNAL_USER_DATA_FETCH_FAIL
from utilities.permissions import IsExternalUser


class DataShareView(GenericAPIView):
    queryset = Request.objects.filter()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsExternalUser)

    def fetch_data(self, condition):
        if condition == 1:
            data = self.get_queryset().values('book__name', 'user__department').\
                annotate(read_count=Count('request_id')).order_by('book__name', 'user__department')
        elif condition == 2:
            data = self.get_queryset().values('book__name', 'user__study_level'). \
                annotate(read_count=Count('request_id')).order_by('book__name', 'user__study_level')
        else:
            data = self.get_queryset().values('book__name', 'user__department', 'user__study_level'). \
                annotate(read_count=Count('request_id')).order_by('book__name', 'user__department', 'user__study_level')
        return data

    def get(self, request, *args, **kwargs):
        """
        API to get aggregated data
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            get_filter = request.GET.get('filter', 3)
            data = self.fetch_data(int(get_filter))
            data_frame = pd.DataFrame(list(data))
            url = create_df_csv(data_frame, get_filter)
            data = create_response_dict({"file": url}, EXTERNAL_USER_DATA_FETCH_SUCCESS, True)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = create_response_dict(str(e), EXTERNAL_USER_DATA_FETCH_FAIL, False)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
