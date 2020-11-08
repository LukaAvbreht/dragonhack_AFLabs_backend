from django.shortcuts import render
from rest_framework import viewsets, mixins
from pasovcek.models import Nesreca, Oseba
from pasovcek.models import KlasifikacijaNesrece, Lokacija, VrstaCeste, VzrokNesrece, TipNesrece, VremenskeOkoliscine, StanjePrometa, VrstaPrometa, StanjeVozisca, VrstaVozisca, UpravnaEnotaStoritve, OpisKraja
from pasovcek.serializers import KlasifikacijaSerializer, LokacijaSerializer, VrstaCesteSerializer, VzrokNesreceSerializer, TipNesreceSerializer, VremenskeOkoliscineSerializer, StanjePrometaSerializer, VrstaPrometaSerializer, StanjeVoziscaSerializer, VrstaVoziscaSerializer, UpravnaEnotaStoritveSerializer, OpisKrajaSerializer
from pasovcek.serializers import NesrecaSerializer, NesrecaSerializerGeolocation, OsebaSerializer
from pasovcek.models import TextCesteNaselja
from pasovcek.serializers import TextCesteNaseljaSerializer
from pasovcek.utils import mesecna_statistika_cache
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
import requests
import re
from datetime import datetime, date, timedelta

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

        year = self.request.query_params.get("year", None)
        if year is not None:
            nesrece = nesrece.filter(datum__year=year)

        filters = ["lokacija","vrsta_ceste","sifra_ceste","text_ceste_naselja","sifra_odseka_ulice",
                   "text_odseka_ulice","stacionaza_dogodka","opis_kraja","vzrok_nesrece","tip_nesrece",
                   "vremenske_okoliscine","stanje_prometa","stanje_vozisca","vrsta_vozisca"]
        for filter in filters:
            if self.request.query_params.get(filter, None) is not None:
                nesrece = nesrece.filter(**{filter: self.request.query_params.get(filter, None)})

        starost_min = self.request.query_params.get("povzrocitelj_starost_min", None)
        starost_max = self.request.query_params.get("povzrocitelj_starost_max", None)
        if starost_min is not None and starost_max is not None:
            nesrece = nesrece.filter(udelezenci__je_povzrocitelj=True, udelezenci__starost__gte=int(starost_min), udelezenci__starost__lte=int(starost_max))
        elif starost_min is not None:
            nesrece = nesrece.filter(udelezenci__je_povzrocitelj=True, udelezenci__starost__gte=int(starost_min))
        elif starost_max is not None:
            nesrece = nesrece.filter(udelezenci__je_povzrocitelj=True, udelezenci__starost__lte=int(starost_max))

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
        lat = float(request.query_params.get("lat", 46.056946))
        lon = float(request.query_params.get("lon", 14.505751))
        x = float(request.query_params.get("x", 0.03))
        y = float(request.query_params.get("y", 0.03))
        address = request.query_params.get("address", None)
        address_id = request.query_params.get("address_id", None)
        if address is not None or address_id is not None:
            if address_id is not None:
                address = TextCesteNaselja.objects.get(pk=address_id).ime
            r = requests.get("https://maps.googleapis.com/maps/api/geocode/json",
                             params={"key": "AIzaSyBnGvM0xkLCQV7z7okLx42ieOhM1vqVIok", "address": address})
            try:
                lat = r.json()['results'][0]['geometry']['location']['lat']
                lon = r.json()['results'][0]['geometry']['location']['lng']
            except:
                pass

        nesrece = self.get_queryset().filter(lat__gte=lat-x, lat__lte=lat+x, long__gte=lon-y, long__lte=lon+y)
        #paginator = LimitOffsetPagination()
        #pnesrece = paginator.paginate_queryset(nesrece, request)
        serializer = NesrecaSerializerGeolocation(nesrece, many=True)
        return Response({"locations": serializer.data, "lat": lat, "long": lon})

    @action(methods=["GET"], detail=False)
    def letna_statistika(self, request, *args, **kwargs):
        year = 2000
        data = {}
        while True:
            start_date = date(year, 1, 1)
            end_date = date(year + 1, 1, 1)
            year += 1
            nesreces = Nesreca.objects.filter(datum__gte=start_date, datum__lt=end_date)
            data[start_date.strftime('%Y-%m-%d')] = nesreces.count()
            if start_date.strftime('%Y-%m-%d') == '2020-01-01':
                break
        return Response(data)

    @action(methods=["get"], detail=False)
    def mesecna_statistika(self, request, *args, **kwargs):
        year = 2000
        month = 1
        data = {}
        data = mesecna_statistika_cache()
        while False:
            start_date = date(year, month, 1)
            if month == 12:
                year+=1
                month = 0
            end_date = date(year, month+1, 1)
            month += 1
            nesreces = Nesreca.objects.filter(datum__gte=start_date, datum__lt=end_date)
            data[start_date.strftime('%Y-%m-%d')] = nesreces.count()
            if start_date.strftime('%Y-%m-%d') == '2020-08-01':
                break

        return Response(data)

    @action(methods=["get"], detail=False)
    def statistics(self, request, *args, **kwargs):
        models = [KlasifikacijaNesrece, Lokacija, VrstaCeste, VzrokNesrece, TipNesrece, VremenskeOkoliscine,
                  StanjePrometa, VrstaPrometa, StanjeVozisca, VrstaVozisca, UpravnaEnotaStoritve, OpisKraja]
        mnames = [m.__name__ for m in models]

        data = {}
        stats = request.query_params.get("stats", None)
        if stats is not None and stats == 'spol':
            data[0] = self.get_queryset().filter(udelezenci__je_povzrocitelj=True, udelezenci__spol__gte=0).count()
            data[1] = self.get_queryset().filter(udelezenci__je_povzrocitelj=True, udelezenci__spol__gte=1).count()

        if stats is not None and stats == 'starost':
            starost_interval = int(request.query_params.get("starost_interval", 10))
            for i in range(0, 120, starost_interval):
                data[i] = self.get_queryset().filter(udelezenci__je_povzrocitelj=True, udelezenci__starost__gte=i,
                                                     udelezenci__starost__lt=i+starost_interval).count()

        if stats is not None and stats in mnames:
            m = models[mnames.index(stats)]
            t_name = re.sub(r'(?<!^)(?=[A-Z])', '_', m.__name__).lower()
            objs = m.objects.all()
            for obj in objs:
                data[obj.ime] = self.get_queryset().filter(**{t_name: obj}).count()

        return Response(data)


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