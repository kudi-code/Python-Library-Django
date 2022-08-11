from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookItemViewSet

router = DefaultRouter()
router.register("books", BookViewSet)
router.register("bookItems", BookItemViewSet)
urls = router.urls

urlpatterns = urls