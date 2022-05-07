from django.urls import path
from rest_framework import routers

from library_app.views.student import BookViewSet, ProfileView, RequestViewSet, ReserveViewSet

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'reserve', ReserveViewSet)

urlpatterns = [
    path('profile', ProfileView.as_view(), name='student_profile')
]
urlpatterns += router.urls
