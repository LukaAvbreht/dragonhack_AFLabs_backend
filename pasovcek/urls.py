from rest_framework.routers import DefaultRouter
from pasovcek.views import NesrecaViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"nesrece", NesrecaViewSet, basename="nesrece")


urlpatterns = [*router.urls]
