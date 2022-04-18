from rest_framework import routers

from library_app.views.student import BookViewSet

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)

urlpatterns = []
urlpatterns += router.urls
