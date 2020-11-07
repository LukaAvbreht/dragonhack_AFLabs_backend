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
        nesrece = Nesreca.objects.all()

        datum_gte = self.request.query_params.get("datum_gte", None)
        if datum_gte is not None:
            nesrece = nesrece.filter(datum__gte=datum_gte)
        datum_lte = self.request.query_params.get("datum_lte", None)
        if datum_lte is not None:
            nesrece = nesrece.filter(datum__lte=datum_lte)

        filters = ["lokacija","vrsta_ceste","sifra_ceste","text_ceste_naselja","sifra_odseka_ulice",
                   "text_odseka_ulice","stacionaza_dogodka","opis_kraja","vzrok_nesrece","tip_nesrece",
                   "vremenske_okoliscine","stanje_prometa","stanje_vozisca","vrsta_vozisca"]
        for filter in filters:
            if self.request.query_params.get(filter, None) is not None:
                nesrece = nesrece.filter(**{filter: self.request.query_params.get(filter, None)})

        return nesrece
    
    @action(methods=["GET"], detail=False)
    def letna_statistika(self, request, *args, **kwargs):
        return Response("Tu bo prišla letna statistika")

    @action(methods=["get"], detail=False)
    def mesecna_statistika(self, request, *args, **kwargs):
        return Response("Tu bo prišla mesečna statistika")

class OsebaViewSet(viewsets.GenericViewSet,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin):

    queryset = Oseba.objects.all()
    serializer_class = OsebaSerializer

    def get_queryset(self):
        return super().get_queryset()

