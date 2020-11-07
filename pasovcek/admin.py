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

@admin.register(TextCesteNaselja)
class TextCesteNaseljaAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")
    search_fields = ["pk"]

@admin.register(TextOdsekaUlice)
class TextOdsekaUliceAdmin(admin.ModelAdmin):
    list_display = ("pk", "ime")
    search_fields = ["pk"]


@admin.register(Oseba)
class OsebaAdmin(admin.ModelAdmin):
    list_display = ("vrsta_udelezenca", "je_povzrocitelj", "starost", "spol",
                    # "poskodba", "vozniski_staz",
                    "vrednost_alkotesta", "drzavljanstvo", "ue_prebivalisca",
                    "nesreca__text_ceste_naselja__ime",
                    # "nesreca__text_odseka_ulice__ime",
                    "nesreca__vzrok_nesrece__ime", "nesreca__tip_nesrece__ime")
    list_filter = ("spol", "je_povzrocitelj", "drzavljanstvo", "poskodba", "vrsta_udelezenca", "ue_prebivalisca")
    autocomplete_fields = ["nesreca"]

    def nesreca__text_ceste_naselja__ime(self, obj):
        return obj.nesreca.text_ceste_naselja.ime

    def nesreca__text_odseka_ulice__ime(self, obj):
        return obj.nesreca.text_odseka_ulice.ime

    def nesreca__vzrok_nesrece__ime(self, obj):
        return obj.nesreca.vzrok_nesrece.ime

    def nesreca__tip_nesrece__ime(self, obj):
        return obj.nesreca.tip_nesrece.ime


@admin.register(Nesreca)
class NesrecaAdmin(admin.ModelAdmin):
    list_display = ("zaporedna_stevilka", "klasifikacija", "datum", "ura", "v_naselju", "lokacija",
    "vzrok_nesrece", "tip_nesrece")

    list_filter = ("ura", "klasifikacija", "vrsta_ceste", "vzrok_nesrece", "tip_nesrece")
    search_fields = ["pk"]
    autocomplete_fields = ["text_ceste_naselja", "text_odseka_ulice"]
