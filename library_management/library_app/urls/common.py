from django.urls import path

from library_app.views.common import UserLogin

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
]
