from collections import defaultdict
from datetime import date
from typing import Tuple, List, Set
import os.path
from django.core.management.base import BaseCommand
from django.db import connection

import csv

from pasovcek.models import *


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--file_location", type=str)

    def handle(self, *args, **options):
        filename = options["file_location"]
        *_, year = os.path.split(filename)
        year = int(year[2:2 + 4])

        reader = csv.DictReader(open(filename, encoding="cp1252"),
                                delimiter=";")

        def m_g(mdl):
            # def get_me(name):
            #    return mdl.objects.get_or_create(ime=name)[0]
            return lambda name: mdl.objects.get_or_create(ime=name)[0]

        class DefDict(defaultdict):
            def __init__(self, model):
                super().__init__(None)
                self.model = model

            def __missing__(self, key):
                val = self.model.objects.get_or_create(ime=key.strip())[0]
                self[key] = val
                return val

        k_dict = DefDict(KlasifikacijaNesrece)
        u_dict = DefDict(UpravnaEnotaStoritve)
        loc_dict = DefDict(Lokacija)
        v_ceste_dict = DefDict(VrstaCeste)
        sifra_ceste_dict = DefDict(SifraCeste)
        text_naselja_dict = DefDict(TextCesteNaselja)

        sifra_odseka_dict = DefDict(SifraOdsekaUlice)
        text_odseka_dict = DefDict(TextOdsekaUlice)
        stacionaza_dict = DefDict(StacionazaDogodka)
        opis_kraja_dict = DefDict(OpisKraja)

        vzrok_dict = DefDict(VzrokNesrece)
        tip_dict = DefDict(TipNesrece)

        vremenske_ok_dict = DefDict(VremenskeOkoliscine)
        stanje_prom_dict = DefDict(StanjePrometa)
        stanje_voz_dict = DefDict(StanjeVozisca)
        vrsta_voz_dict = DefDict(VrstaVozisca)

        poskodbe_dict = DefDict(TipPoskodbe)
        vrsta_ud_dict = DefDict(VrstaUdelezenca)
        drzav_dict = DefDict(Drzavljanstvo)


        for line in reader:
            # print(line)
            zap_st = line["ZaporednaStevilkaPN"] + "_" + str(year)
            klas = k_dict[line["KlasifikacijaNesrece"]]
            ue_stor = u_dict[line["UpravnaEnotaStoritve"]]
            dat = line["DatumPN"]
            datum = dat[6:] + "-" + dat[3:5] + "-" + dat[:2]
            # print(datum, zap_st)
            ura = line["UraPN"]
            v_naselju = line["VNaselju"]
            assert v_naselju in ["DA", "NE"]
            v_naselju = v_naselju == "DA"
            lok = loc_dict[line["Lokacija"]]

            vrsta_ceste = v_ceste_dict[line["VrstaCesteNaselja"]]
            sifra_ceste = sifra_ceste_dict[line["SifraCesteNaselja"]]
            text_naselja = text_naselja_dict[line["TekstCesteNaselja"]]

            sifra_odseka = sifra_odseka_dict[line["SifraOdsekaUlice"]]
            text_odseka = text_odseka_dict[line["TekstOdsekaUlice"]]

            stacionaza = stacionaza_dict[line["StacionazaDogodka"]]
            opis_kraja = opis_kraja_dict[line["OpisKraja"]]

            vzrok = vzrok_dict[line["VzrokNesrece"]]
            tip = tip_dict[line["TipNesrece"]]

            vremenske = vremenske_ok_dict[line["VremenskeOkoliscine"]]
            stanje_prometa = stanje_prom_dict[line["StanjePrometa"]]
            stanje_vozisca = stanje_voz_dict[line["StanjeVozisca"]]
            vrsta_vozisca = vrsta_voz_dict[line["VrstaVozisca"]]

            geo_x = float(line["GeoKoordinataX"])
            geo_y = float(line["GeoKoordinataY"])

            nes = Nesreca.objects.get_or_create(
                zaporedna_stevilka=zap_st, defaults=dict(
                    klasifikacija=klas, ue_storitve=ue_stor, datum=datum,
                    ura=ura + ":00", v_naselju=v_naselju, lokacija=lok,
                    vrsta_ceste=vrsta_ceste,
                    sifra_ceste=sifra_ceste, text_ceste_naselja=text_naselja,
                    sifra_odseka_ulice=sifra_odseka,
                    text_odseka_ulice=text_odseka,
                    stacionaza_dogodka=stacionaza,
                    opis_kraja=opis_kraja, vzrok_nesrece=vzrok, tip_nesrece=tip,
                    vremenske_okoliscine=vremenske,
                    stanje_prometa=stanje_prometa,
                    stanje_vozisca=stanje_vozisca, vrsta_vozisca=vrsta_vozisca,
                    geo_x=geo_x, geo_y=geo_y,
                )
            )

            vpn = line["ZaporednaStevilkaOsebeVPN"]
            je_povr = line["Povzrocitelj"] == "POVZROČITELJ"
            star = int(line["Starost"])
            spol = line["Spol"] == "ŽENSKA"
            posk = poskodbe_dict[line["PoskodbaUdelezenca"]]
            vrsta_ud = vrsta_ud_dict[line["VrstaUdelezenca"]]

            vozniski_staz = int(line["VozniskiStazVLetih"]) + \
                            int(line["VozniskiStazVMesecih"])/12

            pas = {"DA": True, "NE": False, "NEZNANO": None, "": None}[line["UporabaVarnostnegaPasu"]]

            drz = drzav_dict[line["Drzavljanstvo"]]
            oseba = Oseba.objects.create(
                zaporedna_stevilka=zap_st, nesreca=nes[0],
                vpn_stevilka=vpn, je_povzrocitelj=je_povr, starost=star,
                spol=spol, poskodba=posk, vrsta_udelezenca=vrsta_ud,
                vozniski_staz=vozniski_staz, uporaba_pasu=pas,
                vrednost_alkotesta=float(line["VrednostAlkotesta"].replace(",", ".")),
                strokovni_pregled=float(line["VrednostStrokovnegaPregleda"].replace(",", ".")),
                drzavljanstvo=drz, ue_prebivalisca=u_dict[line["UEStalnegaPrebivalisca"]]
            )

            pass
