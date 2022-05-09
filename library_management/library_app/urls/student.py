from django.urls import path
from rest_framework import routers

from library_app.views.student import BookViewSet, ProfileView, RequestViewSet, ReserveViewSet, ForgottenView

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'reserve', ReserveViewSet)

urlpatterns = [
    path('profile', ProfileView.as_view(), name='student_profile'),
    path('forgotten/', ForgottenView.as_view(), name='student_forgotten')
]
urlpatterns += router.urls
