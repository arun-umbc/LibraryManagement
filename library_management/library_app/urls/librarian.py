from rest_framework import routers

from library_app.views.librarian import BookViewSet, RequestViewSet

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = []
urlpatterns += router.urls
