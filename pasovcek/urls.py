from rest_framework.routers import DefaultRouter
from pasovcek.views import NesrecaViewSet, OsebaViewSet, OtherViewSet, TextCesteNaseljaViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"nesrece", NesrecaViewSet, basename="nesrece")
router.register(r"osebe", OsebaViewSet, basename="osebe")
router.register(r"other", OtherViewSet, basename="other")
router.register(r"text_ceste_naselja", TextCesteNaseljaViewSet, basename="text_ceste_naselja")

urlpatterns = [*router.urls]
