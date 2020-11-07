from django.shortcuts import render
from rest_framework import viewsets, mixins
from pasovcek.models import Nesreca
from pasovcek.serializers import NesrecaSerializer

class NesrecaViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
        
    queryset = Nesreca.objects.all()
    serializer_class = NesrecaSerializer

    def get_queryset(self):
        return super().get_queryset()
    