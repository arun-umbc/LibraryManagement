from django.urls import path
from rest_framework import routers

from library_app.views.external_user import DataShareView

router = routers.SimpleRouter()

urlpatterns = [
    path('data_share', DataShareView.as_view(), name='data_share')
]
urlpatterns += router.urls
