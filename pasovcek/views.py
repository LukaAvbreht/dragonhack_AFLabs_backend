from django.shortcuts import render
from rest_framework import viewsets, mixins
from pasovcek.models import Nesreca, Oseba
from pasovcek.serializers import NesrecaSerializer, OsebaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class NesrecaViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
        
    queryset = Nesreca.objects.all()
    serializer_class = NesrecaSerializer

    def get_queryset(self):
        return super().get_queryset()
    
    @action(methods=["GET"], detail=False)
    def letna_statistika(self, request, *args, **kwargs):
        return Response("Tu bo prišla letna statistika")

    @action(methods=["get"], detail=False)
    def mesecna_statistika(self, request, *args, **kwargs):
        return Reponse("Tu bo prišla mesečna statistika")

class OsebaViewSet(viewsets.GenericViewSet,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin):

    queryset = Oseba.objects.all()
    serializer_class = OsebaSerializer

    def get_queryset(self):
        return super().get_queryset()

