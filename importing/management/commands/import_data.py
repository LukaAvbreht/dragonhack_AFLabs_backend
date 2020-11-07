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
                for m in model.objects.all():
                    self[m.ime] = m

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

        nesrece_dict = {}
        osebe = []

        for j, line in enumerate(reader):
            if not j % 100:
                print(j)
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

            if zap_st in nesrece_dict:
                nesreca = nesrece_dict[zap_st]
            else:
                if geo_x:
                    lat, long, _ = convert(geo_x, geo_y)
                else:
                    lat = long = 0.0
                nesrece_dict[zap_st] = nesreca = Nesreca(zaporedna_stevilka=zap_st,
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
                    geo_x=geo_x, geo_y=geo_y, lat=lat, long=long
                )

            vpn = line["ZaporednaStevilkaOsebeVPN"]
            je_povr = line["Povzrocitelj"] != "UDELEŽENEC"
            star = int(line["Starost"])
            spol = line["Spol"] == "ŽENSKI"
            posk = poskodbe_dict[line["PoskodbaUdelezenca"]]
            vrsta_ud = vrsta_ud_dict[line["VrstaUdelezenca"]]

            vozniski_staz = int(line["VozniskiStazVLetih"]) + \
                            int(line["VozniskiStazVMesecih"])/12

            pas = {"DA": True, "NE": False, "NEZNANO": None, "": None}[line["UporabaVarnostnegaPasu"]]

            drz = drzav_dict[line["Drzavljanstvo"]]
            osebe.append(Oseba(
                zaporedna_stevilka=zap_st, nesreca=nesreca,
                vpn_stevilka=vpn, je_povzrocitelj=je_povr, starost=star,
                spol=spol, poskodba=posk, vrsta_udelezenca=vrsta_ud,
                vozniski_staz=vozniski_staz, uporaba_pasu=pas,
                vrednost_alkotesta=float(line["VrednostAlkotesta"].replace(",", ".")),
                strokovni_pregled=float(line["VrednostStrokovnegaPregleda"].replace(",", ".")),
                drzavljanstvo=drz, ue_prebivalisca=u_dict[line["UEStalnegaPrebivalisca"]]
            ))

        Nesreca.objects.bulk_create(list(nesrece_dict.values()))
        Oseba.objects.bulk_create(osebe)

import math

def convert(x, y, h=0):
    Math = math
    Math.PI = math.pi
    wgs84_a = 6378137.0;

    wgs84_a2 = 40680631590769;

    wgs84_b = 6356752.314;

    wgs84_b2 = 40408299981544.4;

    wgs84_e2 = 0.00669438006676466;

    wgs84_e2_ = 0.00673949681993606;

    bessel_a = 6377397.155;

    bessel_a2 = 40671194472602.1;

    bessel_b = 6356078.963;

    bessel_b2 = 40399739783891.2;

    bessel_e2 = 0.00667437217497493;

    bessel_e2_ = 0.00671921874158131;

    bessel_e4 = 4.45472439300796e-05;

    bessel_e6 = 2.97324885358744e-07;

    bessel_e8 = 1.98445694176601e-09;

    dX = -409.520465;

    dY = -72.191827;

    dZ = -486.872387;

    Alfa = 1.49625622332431e-05;

    Beta = 2.65141935723559e-05;

    Gama = -5.34282614688910e-05;

    dm = -17.919456e-6;

    M0 = [1.0, Math.sin(Gama), -1 * Math.sin(Beta)]

    M1 = [-1 * Math.sin(Gama), 1, Math.sin(Alfa)]

    M2 = [Math.sin(Beta), -Math.sin(Alfa), 1]

    E = 4.76916455578838e-12;

    D = 3.43836164444015e-9

    C = 2.64094456224583e-6;

    B = 0.00252392459157570;

    A = 1.00503730599692;

    y = (y - 500000) / 0.9999;
    x = (1 * x + 5000000) / 0.9999;

    ab = (1 * bessel_a + 1 * bessel_b);
    fi0 = (2 * x) / ab;

    dif = 1.0;
    p1 = bessel_a * (1 - bessel_e2);

    n = 25;
    while (abs(dif) > 0 and n > 0):
        L = p1 * (A * fi0 - B * Math.sin(2 * fi0) + C * Math.sin(
            4 * fi0) - D * Math.sin(6 * fi0) + E * Math.sin(8 * fi0));
        dif = (2 * (x - L) / ab);
        fi0 = fi0 + dif;
        n -= 1;

    N = bessel_a / (Math.sqrt(1 - bessel_e2 * Math.pow(Math.sin(fi0), 2)));
    t = Math.tan(fi0);
    t2 = Math.pow(t, 2);
    t4 = Math.pow(t2, 2);
    cosFi = Math.cos(fi0);
    ni2 = bessel_e2_ * Math.pow(cosFi, 2);
    lam = 0.261799387799149 + (y / (N * cosFi)) - (
            ((1 + 2 * t2 + ni2) * Math.pow(y,
                                           3)) / (6 * Math.pow(N,
                                                               3) * cosFi)) + (
                  ((5 + 28 * t2 + 24 * t4) * Math.pow(y,
                                                      5)) / (
                          120 * Math.pow(N, 5) * cosFi));

    fi = fi0 - ((t * (1 + ni2) * Math.pow(y, 2)) / (2 * Math.pow(N,
                                                                 2))) + (
                 t * (5 + 3 * t2 + 6 * ni2 - 6 * ni2 * t2) * Math.pow(y,
                                                                      4)) / (
                 24 * Math.pow(N, 4)) - (
                 t * (61 + 90 * t2 + 45 * t4) * Math.pow(y,
                                                         6)) / (
                 720 * Math.pow(N, 6));

    N = bessel_a / (Math.sqrt(1 - bessel_e2 * Math.pow(Math.sin(fi), 2)));
    X = (N + h) * Math.cos(fi) * Math.cos(lam);
    Y = (N + h) * Math.cos(fi) * Math.sin(lam);
    Z = ((bessel_b2 / bessel_a2) * N + h) * Math.sin(fi);

    X -= dX;
    Y -= dY;
    Z -= dZ;
    X /= (1 + dm);
    Y /= (1 + dm);
    Z /= (1 + dm);

    X1 = X - M0[1] * Y - M0[2] * Z;
    Y1 = -1 * M1[0] * X + Y - M1[2] * Z;
    Z1 = -1 * M2[0] * X - M2[1] * Y + Z;

    p = Math.sqrt(Math.pow(X1, 2) + Math.pow(Y1, 2));
    O = Math.atan2(Z1 * wgs84_a, p * wgs84_b);
    SinO = Math.sin(O);
    Sin3O = Math.pow(SinO, 3);
    CosO = Math.cos(O);
    Cos3O = Math.pow(CosO, 3);

    fif = Math.atan2(Z1 + wgs84_e2_ * wgs84_b * Sin3O,
                     p - wgs84_e2 * wgs84_a * Cos3O);
    lambdaf = Math.atan2(Y1, X1);

    N = wgs84_a / Math.sqrt(1 - wgs84_e2 * Math.pow(Math.sin(fif), 2));
    hf = p / Math.cos(fif) - N;

    fif = (fif * 180) / Math.PI;
    lambdaf = (lambdaf * 180) / Math.PI;

    retVal = fif, lambdaf, hf
    # print(time.time() - tt)
    # Tak vrstni red, kot rabi google maps
    return retVal
