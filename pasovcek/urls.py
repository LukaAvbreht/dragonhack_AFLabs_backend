from rest_framework.routers import DefaultRouter
from pasovcek.views import NesrecaViewSet, OsebaViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"nesrece", NesrecaViewSet, basename="nesrece")
router.register(r"osebe", NesrecaViewSet, basename="osebe")

urlpatterns = [*router.urls]
