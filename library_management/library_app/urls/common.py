from django.urls import path

from library_app.views.common import UserLogin, SignUp

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup')
]
