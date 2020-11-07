from rest_framework import serializers
from pasovcek.models import *

class KlasifikacijaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlasifikacijaNesrece
        fields = ("id", "ime")

class LokacijaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lokacija
        fields = ("id", "ime")

class VrstaCesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaCeste
        fields = ("id", "ime")

class SifraCesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SifraCeste
        fields = ("id", "ime")

class SifraOdsekaUliceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SifraOdsekaUlice
        fields = ("id", "ime")

class VzrokNesreceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VzrokNesrece
        fields = ("id", "ime")

class TipNesreceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipNesrece
        fields = ("id", "ime")

class VremenskeOkoliscineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VremenskeOkoliscine
        fields = ("id", "ime")

class StanjePrometaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StanjePrometa
        fields = ("id", "ime")

class StanjeVoziscaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StanjeVozisca
        fields = ("id", "ime")

class VrstaVoziscaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaVozisca
        fields = ("id", "ime")

class OsebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oseba
        fields = ("id", "zaporedna_stevilka", "nesreca", "vpn_stevilka", "je_povzrocitelj",
        "starost", "spol", "poskodba", "vrsta_udelezenca", "vozniski_staz", "uporaba_pasu", "vrednost_alkotesta",
        "strokovni_pregled", "drzavljanstvo")


class NesrecaSerializer(serializers.ModelSerializer):
    klasifikacija = KlasifikacijaSerializer(many=False)
    lokacija = LokacijaSerializer(many=False)
    vrsta_ceste = VrstaCesteSerializer(many=False)
    sifra_ceste = SifraCesteSerializer(many=False)
    sifra_odseka_ulice = SifraOdsekaUliceSerializer(many=False)
    vzrok_nesrece = VzrokNesreceSerializer(many=False)
    tip_nesrece = TipNesreceSerializer(many=False)
    vremenske_okoliscine = VremenskeOkoliscineSerializer(many=False)
    stanje_prometa = StanjePrometaSerializer(many=False)
    stanje_vozisca = StanjeVoziscaSerializer(many=False)
    vrsta_vozisca = VrstaVoziscaSerializer(many=False)
    udelezenci = OsebaSerializer(many=True)

    class Meta:
        model = Nesreca
        fields = ("zaporedna_stevilka", "klasifikacija", "datum", "ura", "v_naselju",
        "lokacija", "vrsta_ceste", "sifra_ceste", "sifra_odseka_ulice", "vzrok_nesrece",
        "tip_nesrece", "vremenske_okoliscine", "stanje_prometa", "stanje_vozisca", "vrsta_vozisca",
        "geo_x", "geo_y", "udelezenci")