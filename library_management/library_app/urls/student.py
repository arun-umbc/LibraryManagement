from django.urls import path
from rest_framework import routers

from library_app.views.student import BookViewSet, ProfileView

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('profile', ProfileView.as_view(), name='student_profile')
]
urlpatterns += router.urls
