from django.shortcuts import render
from rest_framework import viewsets, mixins
from pasovcek.models import Nesreca, Oseba
from pasovcek.models import KlasifikacijaNesrece, Lokacija, VrstaCeste, VzrokNesrece, TipNesrece, VremenskeOkoliscine, StanjePrometa, VrstaPrometa, StanjeVozisca, VrstaVozisca, UpravnaEnotaStoritve, OpisKraja
from pasovcek.serializers import KlasifikacijaSerializer, LokacijaSerializer, VrstaCesteSerializer, VzrokNesreceSerializer, TipNesreceSerializer, VremenskeOkoliscineSerializer, StanjePrometaSerializer, VrstaPrometaSerializer, StanjeVoziscaSerializer, VrstaVoziscaSerializer, UpravnaEnotaStoritveSerializer, OpisKrajaSerializer
from pasovcek.serializers import NesrecaSerializer, NesrecaSerializerGeolocation, OsebaSerializer
from pasovcek.models import TextCesteNaselja
from pasovcek.serializers import TextCesteNaseljaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

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

        starost = self.request.query_params.get("povzrocitelj_starost", None)
        if starost is not None:
            starost = int(starost)
            nesrece = nesrece.filter(udelezenci__je_povzrocitelj=True, udelezenci__starost__gte=starost, udelezenci__starost__lte=starost+10)

        alkohol = self.request.query_params.get("povzrocitelj_alkohol", None)
        if alkohol is not None:
            alkohol = float(alkohol)
            nesrece = nesrece.filter(udelezenci__je_povzrocitelj=True, udelezenci__vrednost_alkotesta__gte=alkohol)

        spol = self.request.query_params.get("povzrocitelj_spol", None)
        if spol is not None:
            spol = int(spol)
            nesrece = nesrece.filter(udelezenci__je_povzrocitelj=True, udelezenci__spol__gte=spol)

        return nesrece

    @action(methods=["GET"], detail=False)
    def geolocation(self, request, *args, **kwargs):
        lat = float(request.query_params.get("lat", None))
        lon = float(request.query_params.get("lon", None))
        x = float(request.query_params.get("x", None))
        y = float(request.query_params.get("y", None))
        nesrece = self.get_queryset().filter(lat__gte=lat-x, lat__lte=lat+x, long__gte=lon-y, long__lte=lon+y)
        #paginator = LimitOffsetPagination()
        #pnesrece = paginator.paginate_queryset(nesrece, request)
        serializer = NesrecaSerializerGeolocation(nesrece, many=True)
        return Response(serializer.data)
    
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


class TextCesteNaseljaViewSet(viewsets.GenericViewSet,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin):

    queryset = TextCesteNaselja.objects.all()
    serializer_class = TextCesteNaseljaSerializer

    def get_queryset(self):
        texts = TextCesteNaselja.objects.all()

        contains = self.request.query_params.get("contains", None)
        if contains is not None:
            texts = texts.filter(ime__icontains=contains)

        return texts


class OtherViewSet(viewsets.GenericViewSet):
    @action(methods=["GET"], detail=False)
    def other(self, request, *args, **kwargs):
        models = [KlasifikacijaNesrece, Lokacija, VrstaCeste, VzrokNesrece, TipNesrece, VremenskeOkoliscine,
                  StanjePrometa, VrstaPrometa, StanjeVozisca, VrstaVozisca, UpravnaEnotaStoritve, OpisKraja]
        serializers = [KlasifikacijaSerializer, LokacijaSerializer, VrstaCesteSerializer, VzrokNesreceSerializer,
                       TipNesreceSerializer, VremenskeOkoliscineSerializer, StanjePrometaSerializer,
                       VrstaPrometaSerializer, StanjeVoziscaSerializer, VrstaVoziscaSerializer, UpravnaEnotaStoritveSerializer,
                       OpisKrajaSerializer]

        data = {}
        for i, m in enumerate(models):
            objs = m.objects.all()
            data[m.__name__] = serializers[i](objs, many=True).data

        return Response(data)