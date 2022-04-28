from django.urls import path
from rest_framework import routers

from library_app.views.student import BookViewSet, ProfileView, RequestViewSet

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = [
    path('profile', ProfileView.as_view(), name='student_profile')
]
urlpatterns += router.urls
