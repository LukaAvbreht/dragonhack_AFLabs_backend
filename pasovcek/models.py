from django.db import models

# Create your models here.


nb = dict(null=True, blank=True)

class KlasifikacijaNesrece(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime


class UpravnaEnotaStoritve(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime


class Lokacija(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class VrstaCeste(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class TextCesteNaselja(models.Model):
    ime = models.CharField(max_length=192)


class SifraCeste(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class SifraOdsekaUlice(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class TextOdsekaUlice(models.Model):
    ime = models.CharField(max_length=192)


class StacionazaDogodka(models.Model):
    ime = models.CharField(max_length=192)

class OpisKraja(models.Model):
    ime = models.CharField(max_length=192)


class VzrokNesrece(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class TipNesrece(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class VremenskeOkoliscine(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class StanjePrometa(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class VrstaPrometa(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class StanjeVozisca(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class VrstaVozisca(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class Nesreca(models.Model):
    zaporedna_stevilka = models.CharField(max_length=64, **nb)
    klasifikacija = models.ForeignKey(to=KlasifikacijaNesrece,
                                      on_delete=models.PROTECT, **nb)
    ue_storitve = models.ForeignKey(to=UpravnaEnotaStoritve,
                                    on_delete=models.PROTECT, **nb)

    datum = models.DateField(**nb)
    ura = models.TimeField(**nb)
    v_naselju = models.BooleanField(**nb)
    lokacija = models.ForeignKey(on_delete=models.PROTECT, to=Lokacija, **nb)
    vrsta_ceste = models.ForeignKey(on_delete=models.PROTECT, to=VrstaCeste,
                                    **nb)
    sifra_ceste = models.ForeignKey(on_delete=models.PROTECT, to=SifraCeste,
                                    **nb)
    text_ceste_naselja = models.ForeignKey(on_delete=models.PROTECT,
                                           to=TextCesteNaselja, **nb)
    sifra_odseka_ulice = models.ForeignKey(on_delete=models.PROTECT,
                                           to=SifraOdsekaUlice, **nb)
    text_odseka_ulice = models.ForeignKey(on_delete=models.PROTECT,
                                           to=TextOdsekaUlice, **nb)

    stacionaza_dogodka = models.ForeignKey(on_delete=models.PROTECT,
                                   to=StacionazaDogodka, **nb)

    opis_kraja = models.ForeignKey(on_delete=models.PROTECT,
                                   to=OpisKraja, **nb)

    vzrok_nesrece = models.ForeignKey(on_delete=models.PROTECT,
                                      to=VzrokNesrece, **nb)
    tip_nesrece = models.ForeignKey(on_delete=models.PROTECT, to=TipNesrece,
                                    **nb)
    vremenske_okoliscine = models.ForeignKey(on_delete=models.PROTECT,
                                             to=VremenskeOkoliscine, **nb)
    stanje_prometa = models.ForeignKey(on_delete=models.PROTECT,
                                       to=StanjePrometa, **nb)
    stanje_vozisca = models.ForeignKey(on_delete=models.PROTECT,
                                       to=StanjeVozisca, **nb)
    vrsta_vozisca = models.ForeignKey(on_delete=models.PROTECT, to=VrstaVozisca,
                                      **nb)

    geo_x = models.FloatField(**nb)
    geo_y = models.FloatField(**nb)

    lat = models.FloatField(**nb)
    long = models.FloatField(**nb)


class TipPoskodbe(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class VrstaUdelezenca(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime

class Drzavljanstvo(models.Model):
    ime = models.CharField(max_length=192)

    def __str__(self):
        return self.ime
        
class Oseba(models.Model):
    zaporedna_stevilka = models.CharField(max_length=64, **nb)
    nesreca = models.ForeignKey(to=Nesreca, on_delete=models.PROTECT,
                                related_name="udelezenci", **nb)
    vpn_stevilka = models.IntegerField(**nb)
    je_povzrocitelj = models.BooleanField(**nb)
    starost = models.IntegerField(**nb)
    spol = models.IntegerField(choices=[(0, "Moški"), (1, "Ženska")], **nb)
    poskodba = models.ForeignKey(to=TipPoskodbe, on_delete=models.PROTECT, **nb)
    vrsta_udelezenca = models.ForeignKey(to=VrstaUdelezenca,
                                         on_delete=models.PROTECT, **nb)

    vozniski_staz = models.FloatField(**nb)
    uporaba_pasu = models.BooleanField(**nb)  # Neznano je NULL

    vrednost_alkotesta = models.FloatField(**nb)
    strokovni_pregled = models.FloatField(**nb)
    drzavljanstvo = models.ForeignKey(to=Drzavljanstvo,
                                      on_delete=models.PROTECT, **nb)
    ue_prebivalisca = models.ForeignKey(to=UpravnaEnotaStoritve,
                                        on_delete=models.PROTECT, **nb)
