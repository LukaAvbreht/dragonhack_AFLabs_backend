from django.contrib import admin
from pasovcek.models import *

@admin.register(KlasifikacijaNesrece)
class KlasifikacijaNesreceAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(UpravnaEnotaStoritve)
class UpravnaEnotaStoritveAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(Lokacija)
class LokacijaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(VrstaCeste)
class VrstaCesteAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(SifraCeste)
class SifraCesteAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(SifraOdsekaUlice)
class SifraOdsekaUliceAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(VzrokNesrece)
class VzrokNesreceAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(TipNesrece)
class TipNesreceAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(VremenskeOkoliscine)
class VremenskeOkoliscineAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(StanjePrometa)
class StanjePrometaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(VrstaPrometa)
class VrstaPrometaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(StanjeVozisca)
class StanjeVoziscaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(VrstaVozisca)
class VrstaVoziscaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(TipPoskodbe)
class TipPoskodbeAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(VrstaUdelezenca)
class VrstaUdelezencaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")

@admin.register(Drzavljanstvo)
class DrzavljanstvoAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")


@admin.register(Oseba)
class OsebaAdmin(admin.ModelAdmin):
    list_display = ("nesreca", "je_povzrocitelj", "starost", "spol", "poskodba", "vrsta_udelezenca",
    "vozniski_staz", "vrednost_alkotesta", "drzavljanstvo", "ue_prebivalisca")
    list_filter = ("spol", "je_povzrocitelj", "drzavljanstvo", "poskodba", "vrsta_udelezenca", "ue_prebivalisca")

@admin.register(Nesreca)
class NesrecaAdmin(admin.ModelAdmin):
    list_display = ("zaporedna_stevilka", "klasifikacija", "datum", "ura", "v_naselju", "lokacija",
    "vzrok_nesrece", "tip_nesrece")

    list_filter = ("ura", "klasifikacija", "vrsta_ceste", "vzrok_nesrece", "tip_nesrece")
