from rest_framework import routers

from library_app.views.librarian import BookViewSet, RequestViewSet, ReserveViewSet

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'reserve', ReserveViewSet)

urlpatterns = []
urlpatterns += router.urls
